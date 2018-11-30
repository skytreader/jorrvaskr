import app

def insert_fixtures(session):
    from app.models import GameType
    session.add(GameType(label="One Night"))
    session.add(GameType(label="Ultimate"))
    session.commit()

if __name__ == "__main__":
    _app = app.make_app("config.Config")
    insert_fixtures(app.db.session)
