import app

def insert_fixtures(session):
    from app.models import Faction, GameType
    session.add(GameType(id=1,label="One Night"))
    session.add(GameType(id=2, label="Ultimate"))
    session.add(Faction(id=1, name="Werewolves"))
    session.add(Faction(id=2, name="Villagers"))
    session.add(Faction(id=3, name="Tanner"))
    session.add(Faction(id=4, name="Lovers"))
    session.commit()

if __name__ == "__main__":
    _app = app.make_app("config.Config")
    insert_fixtures(app.db.session)
