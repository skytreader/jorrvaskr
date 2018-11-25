from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)

def init_db():
    db.create_all()
    db.session.commit()

@app.route("/")
def index():
    return "Hello World"
