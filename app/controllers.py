from app import app, db
from app.models import Faction, FactionTally, GameSession, GameType
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
    return render_template("records-view.jinja")
