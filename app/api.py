from flask import Blueprint, request
from app import app, db
from app.models import (
    get_or_create, Faction, FactionTally, FactionWinLog, GameSession,
    GameSessionRecord, Player, PlayerWinLog
)

from datetime import datetime, timedelta
from sqlalchemy.sql import func
from sqlalchemy import text

import flask
import app.limits as limits

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
    game_session = GameSession.find_session(session_date, game_type)

    if not game_session:
        # In this sense, `created_at` lies because the date the game was started
        # in the frontend could be different from the time it gets here.
        game_session = GameSession(
            game_type_id=game_type, created_at=session_date
        )
        db.session.add(game_session)
        db.session.flush()

    player_map = {}
    for p in players:
        player_map[p] = get_or_create(Player, name=p)

    game_session.games_played += 1
    game_session.last_modified = datetime.now()

    # Record factions
    faction = get_or_create(Faction, name=faction)
    faction_tally = get_or_create(
        FactionTally, faction_id=faction.id, game_session_id=game_session.id
    )
    faction_tally.games_won += 1
    faction_tally.last_modified = datetime.now()
    faction_win_log = FactionWinLog(faction=faction, game_session=game_session)

    # Record player wins/plays
    player_game_session_records = {}

    for p in players:
        player_game_session_records[p] = get_or_create(
            GameSessionRecord,
            player=player_map[p],
            game_session=game_session
        )
        player_game_session_records[p].games_played += 1
        player_game_session_records[p].last_modified = datetime.now()

        if p in winners:
            player_game_session_records[p].games_won += 1
            player_game_session_records[p].last_modified = datetime.now()
            db.session.add(
                PlayerWinLog(
                    player=player_map[p],
                    faction_win_log=faction_win_log
                )
            )

    db.session.commit()
    return "OK"

@bp.route("/game_record/edit/winlog_old", methods=("POST",))
def edit_winlog_old():
    app.logger.warn(
        "/game_record/edit/winlog_old Deprecated API endpoint called. Should not happen.\n" +
        "This endpoint has wrong logic to begin with. Should only be called in dev."
    )
    winlog_id = int(request.form.get("id"))
    updated_faction = request.form.get("faction")
    # Technically, we should get_or_create here but this endpoint is deprecated
    # either way so meh.
    new_faction = Faction.get_faction_from_name(updated_faction)

    winlog_record = (
        db.session.query(PlayerWinLog)
        .filter(PlayerWinLog.id == winlog_id)
        .first()
    )

    if winlog_record is None:
        return "Nonexistent PlayerWinLog id", 400

    winlog_record.faction_id = new_faction.id
    winlog_record.last_modified = datetime.now()

    db.session.commit()
    return "OK", 200

@bp.route("/game_record/view/factions/<int:game_session_id>")
def get_faction_wins_for_session(game_session_id):
    """
    Returns a JSON object with two fields:

    - "log" is a log of the last 10 factions who won, ordered by who last won.
    - "record_count" is a count of all wins from a faction in this session so
      far.
    """
    raw_records = (
        db.session.query(
            Faction.name
        ).filter(FactionWinLog.game_session_id == game_session_id)
        .filter(FactionWinLog.faction_id == Faction.id)
        .order_by(FactionWinLog.created_at.desc(), FactionWinLog.id.desc())
        .limit(limits.GAME_RECORDS_WINDOW)
    )
    raw_records = [record[0] for record in raw_records]
    counts = (
        db.session.query(
            Faction.name,
            func.count(FactionWinLog.id).label("times_won")
        ).filter(FactionWinLog.game_session_id == game_session_id)
        .filter(FactionWinLog.faction_id == Faction.id)
        .group_by(Faction.name)
        .order_by(text("times_won DESC"))
        .limit(limits.FACTION_TALLY_COUNTS)
    )
    counts = {row[0]: row[1] for row in counts}

    return flask.jsonify({"log": raw_records, "record_count": counts})

@bp.route("/game_session/view/id/<int:game_type_id>")
def get_game_session_id(game_type_id):
    session_date = datetime.fromisoformat(request.args["session-date"])
    return str(GameSession.find_session(session_date, game_type_id).id)

def compute_player_winlog_summary(playerid):
    return (
        db.session.query(
            Faction.name,
            func.count(FactionWinLog.game_session_id).label("win_counts")
        ).filter(PlayerWinLog.player_id == playerid)
        .filter(PlayerWinLog.faction_win_log_id == FactionWinLog.id)
        .filter(FactionWinLog.faction_id == Faction.id)
        .group_by(Faction.name)
        .order_by(text("win_counts DESC"))
        .limit(limits.FACTION_TALLY_COUNTS)
        .all()
    )

def compute_detailed_winlog(playerid):
    return (
        db.session.query(
            PlayerWinLog.id,
            func.to_char(GameSession.created_at, "YYYY-MM-DD"),
            Faction.name
        ).filter(PlayerWinLog.faction_win_log_id == FactionWinLog.id)
        .filter(PlayerWinLog.player_id == playerid)
        .filter(FactionWinLog.game_session_id == GameSession.id)
        .filter(FactionWinLog.faction_id == Faction.id)
        .order_by(GameSession.created_at.desc(), PlayerWinLog.id)
        .all()
    )
