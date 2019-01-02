from flask_testing import TestCase
import app as App
import unittest
import os

class AppTestCase(TestCase):

    def create_app(self):
        app = App.make_app(os.environ.get("JORRVASKR_CONFIG", "config.config"))
        app.config["TESTING"] = True
        return app

    def setUp(self):
        self.app = self.create_app()

    def __delete_table(self, tbl_name):
        # WARNING: Prone to injections. But we are deleting anyway and this is
        # just for tests, never for prod.
        App.db.engine.execute("DELETE FROM %s;" % tbl_name)

    def tearDown(self):
        App.db.session.rollback()
        # FIXME This will complain about foreign keys.
        self.__delete_table("game_types")
        self.__delete_table("players")
        self.__delete_table("game_sessions")
        self.__delete_table("game_session_records")
        self.__delete_table("factions")
        self.__delete_table("faction_tallies")
        self.__delete_table("win_logs")
        self.__delete_table("win_weights")
