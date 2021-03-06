from app import api, db
from app.models import (
    Faction, FactionTally, GameSession, GameSessionRecord, GameType, Player,
    PlayerWinLog
)
from datetime import datetime
from flask import Blueprint, render_template, request
from sqlalchemy.sql import func
from sqlalchemy import text

import json

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
                db.session.query(
                    Faction.name,
                    func.sum(FactionTally.games_won).label("faction_tallies")
                )
                .filter(FactionTally.game_session_id.in_(games))
                .filter(Faction.id == FactionTally.faction_id)
                .group_by(Faction.name)
                .order_by(text("faction_tallies DESC"))
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
    session_date = datetime.fromisoformat(request.form["session-start-date"])
    ultimate_session = GameSession.find_session(
        session_date, GameType.get_gametype_from_label("Ultimate").id
    )
    one_night_session = GameSession.find_session(
        session_date, GameType.get_gametype_from_label("One Night").id
    )
    ultimate_faction_records = (
        json.loads(api.get_faction_wins_for_session(ultimate_session.id).data)
        if ultimate_session is not None else None
    )
    one_night_faction_records = (
        json.loads(api.get_faction_wins_for_session(one_night_session.id).data)
        if one_night_session is not None else None
    )
    return render_template(
        "session-new.jinja",
        session_date=request.form["session-start-date"],
        scripts=("session-new.js",),
        styles=("custom-fancy.css", "session-new.css"),
        factions=factions,
        ultimate_faction_wins=ultimate_faction_records,
        one_night_faction_wins=one_night_faction_records
    )

@bp.route("/records/view")
def records_view():
    game_types = db.session.query(GameType).all()
    records_per_type = {}
    for gt in game_types:
        # TODO Limit this
        records_per_type[gt.label] = (
            db.session.query(
                Player.id,
                Player.name,
                func.sum(GameSessionRecord.games_played).label("games_played"),
                func.sum(GameSessionRecord.games_won).label("games_won")
            ).filter(GameSession.id == GameSessionRecord.game_session_id)
            .filter(GameSession.game_type_id == gt.id)
            .filter(GameSessionRecord.player_id == Player.id)
            .group_by(Player.id, Player.name)
            .order_by(text("games_played DESC"), text("games_won DESC"))
            .all()
        )
    return render_template("records-view.jinja", records=records_per_type)

@bp.route("/records/view/<int:playerid>")
def view_user_record(playerid):
    context = {
        "scripts": ("view-user-record.js",)
    }
    context["player_name"] = (
        db.session.query(Player.name)
        .filter(Player.id == playerid)
        .scalar()
    )

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

    context["winlog_summary"] = api.compute_player_winlog_summary(playerid)
    context["detailed_winlog"] = api.compute_detailed_winlog(playerid)
    context["styles"] = ("view-user-record.css",)

    return render_template("view-user-record.jinja", **context)
