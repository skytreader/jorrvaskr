from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

def make_app(config):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db = SQLAlchemy(app)
    
    db.create_all()
    db.session.commit()

    from .controllers import bp
    app.register_blueprint(bp)
    
    return app
