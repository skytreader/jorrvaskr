import app

def insert_fixtures(session):
    from app.models import Faction, GameType
    session.add(GameType(label="One Night"))
    session.add(GameType(label="Ultimate"))
    session.add(Faction(name="Werewolves"))
    session.add(Faction(name="Villagers"))
    session.add(Faction(name="Tanner"))
    session.add(Faction(name="Lovers"))
    session.commit()

if __name__ == "__main__":
    _app = app.make_app("config.Config")
    insert_fixtures(app.db.session)
