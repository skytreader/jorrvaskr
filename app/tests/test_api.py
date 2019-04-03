from .base import AppTestCase
from .factories import *
from app import db
from app import api
from app.models import Faction, GameSession, GameSessionRecord, GameType, Player
from datetime import datetime
from freezegun import freeze_time

import app.tests.factories as f

FREEZE_DATE = "2019-01-28"

@freeze_time(FREEZE_DATE)
class ApiTests(AppTestCase):

    def setUp(self):
        super(ApiTests, self).setUp()
        self.freeze_time = datetime.strptime(FREEZE_DATE, "%Y-%m-%d")

    def test_game_session_dne(self):
        player_names = ["chad", "je", "shara", "franz", "gelo"]
        game_sessions = (
            self.db.session.query(GameSession)
            .filter(self.freeze_time <= GameSession.created_at)
            .first()
        )
        self.assertTrue(game_sessions is None)
        one_night_game = (
            self.db.session.query(GameType)
            .filter(GameType.label=="One Night")
            .first()
        )
        self.assertTrue(one_night_game is not None)

        for name in player_names:
            self.verify_does_not_exist(Player, name=name)

        rv = self.client.post("/game_record/new",
            data={
                "players": ["chad", "je", "shara", "franz", "gelo"],
                "winners": ["chad"],
                "session-date": datetime.now().isoformat(),
                "game-type": one_night_game.id,
                "faction": "tanner"
            }
        )
        self.assertEqual(200, rv._status_code)
        game_sessions = (
            self.db.session.query(GameSession)
            .filter(self.freeze_time <= GameSession.created_at)
            .first()
        )
        self.assertTrue(game_sessions is not None)
        self.assertEqual(1, game_sessions.games_played)

        for name in player_names:
            self.verify_exists(Player, name=name)

        # Check the GameSessionRecords.
        # Create a map from player name to player object
        actual_player_records = {
            name: (
                self.db.session.query(Player)
                .filter(Player.name == name)
                .first()
            ) for name in player_names
        }

        for name in player_names:
            player_record = (
                self.db.session.query(Player)
                .filter(Player.name == name)
                .first()
            )
            game_session_record = (
                self.db.session.query(GameSessionRecord)
                .filter(GameSessionRecord.game_session_id == game_sessions.id)
                .filter(GameSessionRecord.player_id == player_record.id)
                .first()
            )
            self.assertEqual(1, game_session_record.games_played)
            if name == "chad":
                self.assertEqual(1, game_session_record.games_won)
            else:
                self.assertEqual(0, game_session_record.games_won)

    def test_game_session_exists(self):
        one_night_game = (
            self.db.session.query(GameType)
            .filter(GameType.label=="One Night")
            .first()
        )
        gs = GameSession(game_type=one_night_game, created_at=self.freeze_time)

        existing_players = ["chad", "je"]
        winners = set(["chad"])
        win_play_ratios = [(8, 8), (5, 8)]
        new_players = ["shara", "franz", "gelo"]

        for player, wpr in zip(existing_players, win_play_ratios):
            player_record = PlayerFactory(name=player)
            self.db.session.add(
                GameSessionRecordFactory(
                    player=player_record,
                    game_session=gs,
                    games_won=wpr[0],
                    games_played=wpr[1]
                )
            )
        self.db.session.add(gs)
        self.db.session.flush()
        with self.app.test_request_context("/game_record/new",
            data={
                "players": existing_players + new_players,
                "winners": ["chad"],
                "session-date": datetime.now().isoformat(),
                "game-type": one_night_game.id,
                "faction": "tanner"
            }
        ):
            return_value = api.new_game_records()
            self.assertEqual("OK", return_value)

        game_sessions = (
            self.db.session.query(GameSession)
            .filter(GameSession.game_type_id == one_night_game.id)
            .filter(self.freeze_time <= GameSession.created_at)
            .all()
        )
        self.assertEqual(1, len(game_sessions))
        self.assertEqual(game_sessions[0].id, gs.id)

        for player, wpr in zip(existing_players, win_play_ratios):
            player_record = (
                self.db.session.query(Player)
                .filter(Player.name == player)
                .first()
            )
            game_session_record = (
                self.db.session.query(GameSessionRecord)
                .filter(GameSessionRecord.game_session_id == gs.id)
                .filter(GameSessionRecord.player_id == player_record.id)
                .first()
            )
            self.assertEqual(wpr[1] + 1, game_session_record.games_played)

            if player in winners:
                self.assertEqual(wpr[0] + 1, game_session_record.games_won)
            else:
                self.assertEqual(wpr[0], game_session_record.games_won)

    def test_edit_faction_record(self):
        # Create the records first
        werewolves = Faction.get_faction_from_name("Werewolves")
        villagers = Faction.get_faction_from_name("Villagers")
        self.assertTrue(werewolves is not None)
        self.assertTrue(villagers is not None)
        one_night_game = self.game_type_map["One Night"]

        game_session1 = f.GameSessionFactory(game_type=one_night_game)
        self.db.session.add(f.FactionTallyFactory(
            faction=werewolves, game_session=game_session1, games_won=1
        ))
        self.db.session.add(f.FactionTallyFactory(
            faction=villagers, game_session=game_session1, games_won=2
        ))

        players = (
            "chad", "je", "aya", "mark ian", "josh", "gab", "renzo", "armando",
            "angel", "matthew"
        )

        for idx, name in enumerate(players):
            self.db.session.add(PlayerFactory(id=idx + 1, name=name))

    def test_compute_player_winlog_summary(self):
        # Create player
        player = PlayerFactory()
        self.db.session.add(player)
        self.db.session.flush()
        asc_win_order = ("Villagers", "Lovers", "Werewolves", "Tanner")

        for i, faction in enumerate(asc_win_order):
            win_count = i + 1
            for j in range(win_count):
                fwl = FactionWinLogFactory(
                    faction=Faction.get_faction_from_name(faction)
                )
                self.db.session.add(fwl)
                self.db.session.flush()
                pwl = PlayerWinLogFactory(
                    player=player, faction_win_log=fwl
                )
                self.db.session.add(pwl)
                self.db.session.flush()

        player_winlog_summary = api.compute_player_winlog_summary(player.id)
        factions_len = len(asc_win_order)

        for i, faction in enumerate(reversed(asc_win_order)):
            self.assertEqual(faction, player_winlog_summary[i][0])
            self.assertEqual(factions_len - i, player_winlog_summary[i][1])
