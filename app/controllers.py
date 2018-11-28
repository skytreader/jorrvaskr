from flask import Blueprint, render_template

bp = Blueprint("jorrvaskr", __name__)

@bp.route("/")
def index():
    return render_template("index.jinja")

@bp.route("/session/new/", methods=("GET",))
def session_start():
    return render_template("session-new.jinja")
