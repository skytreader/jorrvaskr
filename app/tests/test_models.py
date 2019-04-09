from .base import AppTestCase
from app.models import GameSession, GameType
from datetime import datetime, timedelta

import app.tests.factories as f

class ModelsTests(AppTestCase):

    def test_find_session_day(self):
        ultimate_werewolf = GameType.get_gametype_from_label("Ultimate")
        self.assertIsNotNone(ultimate_werewolf)
        actual_day = datetime(2019, 4, 9)
        self.assertIsNone(
            GameSession.find_session(actual_day, ultimate_werewolf.id)
        )
        game_session = f.GameSessionFactory(
            created_at=actual_day, game_type=ultimate_werewolf
        )
        self.db.session.add(game_session)
        self.db.session.flush()
        self.assertEqual(
            game_session,
            GameSession.find_session(actual_day, ultimate_werewolf.id)
        )

    def test_find_session_day_edges(self):
        actual_day = datetime(
            2019, 4, 9, hour=0, minute=1
        )
        query_day = actual_day - timedelta(hours=1)
        game_type = GameType.get_gametype_from_label("Ultimate")
        self.assertTrue(game_type is not None)
        self.db.session.add(
            f.GameSessionFactory(created_at=actual_day, game_type=game_type)
        )
        self.db.session.flush()
        self.assertTrue(
            GameSession.find_session(query_day, game_type.id) is None
        )
