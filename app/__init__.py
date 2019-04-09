from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

__PATCH__ = 0
__MINOR__ = 1
__MAJOR__ = 0
__EXT__ = ""
__VERSION__ = "%d.%d.%d%s" % (__MAJOR__, __MINOR__, __PATCH__, __EXT__)

db = None
app = None

def make_app(config):
    global app
    app = Flask(__name__)
    app.config.from_object(config)

    init_db(app)

    from .controllers import bp as controllers_bp
    from .api import bp as api_bp
    app.register_blueprint(controllers_bp)
    app.register_blueprint(api_bp)
    
    return app

def init_db(app):
    global db
    db = SQLAlchemy(app)
    
    from .models import (
        GameType, Player, GameSession, GameSessionRecord, Faction, FactionTally,
        PlayerWinLog, WinWeight
    )
    db.create_all()
    db.session.commit()
    return db
