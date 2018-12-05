from flask import Blueprint, request
from app import app, db
from app.models import (
    get_or_create, Faction, FactionTally, GameSession, GameSessionRecord,
    Player, WinLog
)

from datetime import datetime, timedelta

bp = Blueprint("api", __name__)

@bp.route("/game_record/new", methods=("POST",))
def new_game_records():
    # Retrieve data from the form and assemble them in the proper data type
    # FIXME Cleanup! This is what Flask forms are for!
    players = request.form.getlist("players")
    winners = set(request.form.getlist("winners"))
    session_date = datetime.fromisoformat(request.form["session-date"])
    game_type = int(request.form["game-type"])
    faction = request.form["faction"]
    
    # Find a GameSession, if it exists
    date_query_limit = session_date + timedelta(days=1)
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
        db.session.commit()

    player_map = {}
    for p in players:
        player_map[p] = get_or_create(Player, name=p)

    game_session.games_played += 1

    # Record factions
    faction = get_or_create(Faction, name=faction)
    faction_tally = get_or_create(
        FactionTally, faction_id=faction.id, game_session_id=game_session.id
    )
    faction_tally.games_won += 1

    # Record player wins/plays
    player_game_session_records = {}

    for p in players:
        player_game_session_records[p] = get_or_create(
            GameSessionRecord,
            player=player_map[p],
            game_session=game_session
        )
        player_game_session_records[p].games_played += 1

        if p in winners:
            player_game_session_records[p].games_won += 1
            db.session.add(
                WinLog(
                    player=player_map[p],
                    game_session=game_session,
                    faction=faction
                )
            )

    db.session.commit()
    return "OK"
