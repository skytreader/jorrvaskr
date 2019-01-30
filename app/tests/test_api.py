from .base import AppTestCase
from app import db
from app import api
from app.models import GameSession, GameSessionRecord, GameType, Player
from datetime import datetime
from freezegun import freeze_time

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
        self.db.session.add(gs)
        self.db.session.flush()
        with self.app.test_request_context("/game_record/new",
            data={
                "players": ["chad", "je", "shara", "franz", "gelo"],
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
