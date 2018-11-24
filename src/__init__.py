from flask import Flask

import os

app = Flask(__name__)
app.config.from_object("config.Config")

@app.route("/")
def index():
    return "Hello World"
