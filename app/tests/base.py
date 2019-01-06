from flask_testing import TestCase
import app as App
import unittest
import os

# Here only for all the other initialization stuff which might expect an
# initialized app to be present. In any case, a new app should be created per
# test case.
App.app = App.make_app("config.Config")

class AppTestCase(TestCase):

    def create_app(self):
        app = App.make_app(os.environ.get("JORRVASKR_CONFIG", "config.Config"))
        app.config["TESTING"] = True
        return app

    def setUp(self):
        from app.models import GameType, Faction
        self.app = self.create_app()
        App.db.session.add(GameType(label="One Night"))
        App.db.session.add(GameType(label="Ultimate"))
        App.db.session.add(Faction(name="Werewolves"))
        App.db.session.add(Faction(name="Villagers"))
        App.db.session.add(Faction(name="Tanner"))
        App.db.session.add(Faction(name="Lovers"))
        App.db.session.flush()

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
