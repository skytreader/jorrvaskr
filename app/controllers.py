from app import app
from flask import Blueprint, render_template, request

bp = Blueprint("jorrvaskr", __name__)

@bp.route("/")
def index():
    return render_template("index.jinja")

@bp.route("/session/new", methods=("POST",))
def session_start():
    app.logger.debug(request.form)
    return render_template(
        "session-new.jinja", session_date=request.form["session-start-date"]
    )
