from app import app
from flask import Blueprint, render_template, request

bp = Blueprint("jorrvaskr", __name__)

@bp.route("/")
def index():
    return render_template("index.jinja")

@bp.route("/session/new", methods=("POST",))
def session_start():
    return render_template(
        "session-new.jinja",
        session_date=request.form["session-start-date"],
        scripts=("session-new.js",)
    )
