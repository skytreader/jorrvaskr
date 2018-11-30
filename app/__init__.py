from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

db = None
app = None

def make_app(config):
    global db, app
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db = SQLAlchemy(app)
    
    from .models import (
        GameType, Player, GameSession, GameSessionRecord, Faction, FactionTally,
        WinLog, WinWeight
    )
    db.create_all()
    db.session.commit()

    from .controllers import bp
    app.register_blueprint(bp)
    
    return app
