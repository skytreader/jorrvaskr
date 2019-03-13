from app import app, db
from app.models import (
    Faction, FactionTally, GameSession, GameSessionRecord, GameType, Player,
    WinLog
)
from flask import Blueprint, render_template, request
from sqlalchemy.sql import func

bp = Blueprint("jorrvaskr", __name__)

@bp.route("/")
def index():
    game_types = db.session.query(GameType).all()
    records_per_type = {}
    for gt in game_types:
        games = (
            db.session.query(GameSession.id)
            .filter(GameSession.game_type_id == gt.id)
            .all()
        )
        games = [g[0] for g in games]
        if games:
            records_per_type[gt.label] = (
                db.session.query(Faction.name, func.sum(FactionTally.games_won))
                .filter(FactionTally.game_session_id.in_(games))
                .filter(Faction.id == FactionTally.faction_id)
                .group_by(Faction.name)
                .all()
            )
        else:
            records_per_type[gt.label] = []

    total_games_played = {}
    for gt in game_types:
        total_games_played[gt.label] = (
            db.session.query(func.sum(GameSession.games_played))
            .filter(GameSession.game_type_id == gt.id)
            .scalar()
        )
    return render_template(
        "index.jinja",
        faction_records=records_per_type,
        total_games_played=total_games_played
    )

@bp.route("/session/new", methods=("POST",))
def session_start():
    factions = db.session.query(Faction).all()
    return render_template(
        "session-new.jinja",
        session_date=request.form["session-start-date"],
        scripts=("session-new.js",),
        styles=("custom-fancy.css", "session-new.css"),
        factions=factions
    )

@bp.route("/records/view")
def records_view():
    game_types = db.session.query(GameType).all()
    records_per_type = {}
    for gt in game_types:
        records_per_type[gt.label] = (
            db.session.query(
                Player.name,
                func.sum(GameSessionRecord.games_played),
                func.sum(GameSessionRecord.games_won)
            ).filter(GameSession.id == GameSessionRecord.game_session_id)
            .filter(GameSession.game_type_id == gt.id)
            .filter(GameSessionRecord.player_id == Player.id)
            .group_by(Player.name)
            .all()
        )
    return render_template("records-view.jinja", records=records_per_type)

@bp.route("/records/view/<int:playerid>")
def view_user_record(playerid):
    context = {}
    context["player_name"] = (
        db.session.query(Player.name)
        .filter(Player.id == playerid)
        .scalar()
    )

    # TODO This can be simplified so that we don't need a dictionary anymore.
    played_won_qr = (
        db.session.query(
            GameSession.game_type_id,
            func.sum(GameSessionRecord.games_played),
            func.sum(GameSessionRecord.games_won)
        ).filter(GameSession.id == GameSessionRecord.game_session_id)
        .filter(GameSessionRecord.player_id == playerid)
        .group_by(GameSession.game_type_id)
        .all()
    )
    context["played_won"] = [
        {
            "game_type": GameType.get_label_by_id(pwq[0]),
            "played": pwq[1],
            "won": pwq[2]
        } for pwq in played_won_qr
    ]

    winlog_summary_qr = (
        db.session.query(
            Faction.name,
            func.count(WinLog.game_session_id).label("win_counts")
        ).filter(WinLog.player_id == playerid)
        .filter(WinLog.faction_id == Faction.id)
        .group_by(Faction.name)
        .order_by("win_counts DESC")
        .all()
    )
    context["winlog_summary"] = winlog_summary_qr

    context["detailed_winlog"] = (
        db.session.query(
            GameSession.created_at,
            Faction.name
        ).filter(WinLog.game_session_id == GameSession.id)
        .filter(WinLog.faction_id == Faction.id)
        .filter(WinLog.player_id == playerid)
        .order_by(GameSession.created_at)
        .all()
    )

    return render_template("view-user-record.jinja", **context)
