from .base import AppTestCase
from app import db
from app.models import GameSession
from datetime import datetime
from freezegun import freeze_time

FREEZE_DATE = "2019-01-28"

@freeze_time(FREEZE_DATE)
class ApiTests(AppTestCase):

    def setUp(self):
        super(ApiTests, self).setUp()
        self.freeze_time = datetime.strptime(FREEZE_DATE, "%Y-%m-%d")

    def test_game_session_dne(self):
        game_sessions = (
            db.session.query(GameSession)
            .filter(self.freeze_time <= GameSession.created_at)
            .first()
        )
        self.assertTrue(game_sessions is None)
