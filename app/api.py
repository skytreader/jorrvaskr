from flask import Blueprint, request
from app import app, db
from app.models import (
    get_or_create, Faction, FactionTally, FactionWinLog, GameSession,
    GameSessionRecord, Player, PlayerWinLog
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
        .filter(GameSession.game_type_id == game_type)
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

@bp.route("/game_record/edit/winlog", methods=("POST",))
def edit_winlog():
    winlog_id = int(request.form.get("id"))
    updated_faction = request.form.get("faction")

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
