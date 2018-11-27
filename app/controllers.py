from flask import Blueprint

bp = Blueprint("jorrvaskr", __name__)

@bp.route("/")
def index():
    return "Hello World"
