from flask import Blueprint, request
from app import app, db
from app.models import get_or_create, GameSession, Player

from datetime import datetime, timedelta

bp = Blueprint("api", __name__)

@bp.route("/game_record/new", methods=("POST",))
def new_game_records():
    app.logger.info("the form %s" % request.form)
    players = request.form["players"]
    for p in players:
        get_or_create(Player, name=p)

    game_type = int(request.form["game-type"])
    session_date = datetime.fromisoformat(request.form["session-date"])
    date_query_limit = session_date + timedelta(days=1)
    
    # Find a GameSession, if it exists
    game_session = (
        db.session.query(GameSession)
        .filter(session_date <= GameSession.created_at)
        .filter(GameSession.created_at < date_query_limit)
        .first()
    )

    if not game_session:
        # In this sense, `created_at` lies because the date the game was started
        # in the frontend could be different from the time it gets here.
        game_session = GameSession(
            game_type_id=game_type, created_at=session_date
        )
        db.session.add(game_session)
        db.session.flush()
    return "OK"
