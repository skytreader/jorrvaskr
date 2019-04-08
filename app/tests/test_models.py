from .base import AppTestCase
from app.models import GameSession, GameType
from datetime import datetime, timedelta

import app.tests.factories as f
import arrow

class ModelsTests(AppTestCase):

    def test_find_session_day_edges(self):
        actual_day = arrow.get("2019-04-09 00:01 AM").datetime
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
