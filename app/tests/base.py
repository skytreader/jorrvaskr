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
        _one_night = GameType(label="One Night")
        _ultimate = GameType(label="Utimate")
        self.db.session.add(_one_night)
        self.db.session.add(_ultimate)

        _werewolves = Faction(name="Werewolves")
        _villagers = Faction(name="Villagers")
        _tanner = Faction(name="Tanner")
        _lovers = Faction(name="Lovers")
        self.db.session.add(_werewolves)
        self.db.session.add(_villagers)
        self.db.session.add(_tanner)
        self.db.session.add(_lovers)
        self.db.session.flush()

        self.game_type_map = {
            "One Night": _one_night,
            "Ultimate": _ultimate
        }

        self.faction_map = {
            "Werewolves": _werewolves,
            "Villagers": _villagers,
            "Tanner": _tanner,
            "Lovers": _lovers
        }

    def __delete_table(self, tbl_name):
        # WARNING: Prone to injections. But we are deleting anyway and this is
        # just for tests, never for prod.
        App.db.engine.execute("DELETE FROM %s;" % tbl_name)

    def verify_does_not_exist(self, model, **kwargs):
        """
        Verify that the record described by **kwargs is not yet in the table
        represented by the given model.
        """
        record = self.db.session.query(model).filter_by(**kwargs).first()
        self.assertTrue(record is None)

    def verify_exists(self, model, **kwargs):
        """
        Inverse of verify_does_not_exist.
        """
        record = self.db.session.query(model).filter_by(**kwargs).first()
        self.assertFalse(record is None)

    def tearDown(self):
        App.db.session.rollback()
        # FIXME This will complain about foreign keys.
        # TODO It might suffice to just close the session here. The next test
        # will be on its own session anyway.
        self.__delete_table("game_types")
        self.__delete_table("players")
        self.__delete_table("game_sessions")
        self.__delete_table("game_session_records")
        self.__delete_table("factions")
        self.__delete_table("faction_tallies")
        self.__delete_table("faction_win_logs")
        self.__delete_table("player_win_logs")
        self.__delete_table("win_weights")
