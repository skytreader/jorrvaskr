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
        return App.app

    def setUp(self):
        from app.models import GameType, Faction
        self.app = self.create_app()
        self.db = App.db
        self.db.session.add(GameType(label="One Night"))
        self.db.session.add(GameType(label="Ultimate"))
        self.db.session.add(Faction(name="Werewolves"))
        self.db.session.add(Faction(name="Villagers"))
        self.db.session.add(Faction(name="Tanner"))
        self.db.session.add(Faction(name="Lovers"))
        self.db.session.flush()

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
