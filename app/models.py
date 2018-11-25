from app import db
from sqlalchemy import column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GameType(Base):

    __tablename__ = "game_types"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    last_modified = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )

class Player(Base):

    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    created_at = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    last_modified = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )

class GameSession(Base):

    __tablename__ = "game_sessions"
    id = db.Column(db.Integer, primary_key=True)
    game_type_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "game_types.id", name="gamesession_gametype_fk1", ondelete="CASCADE"
        ),
        nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    last_modified = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )

class GameSessionRecord(Base):

    __tablename__ = "game_session_records"
    __table_args__ = (
        db.CheckConstraint(
            column("games_played") >= column("games_won"),
            name="gamesplayed_geq_gameswon_ck"
        )
    )
    game_session = db.Column(
        db.Integer,
        db.ForeignKey(
            "game_sessions.id", name="gamesessionrecord_gamesessions_fk1",
            ondelete="CASCADE"
        ),
        nullable=False,
        primary_key=True
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "players.id", name="gamesessionrecord_player_fk2",
            ondelete="CASCADE"
        ),
        nullable=False,
        primary_key=True
    )
    games_played = db.Column(
        db.Integer, nullable=False, default=0, server_default=0,
    )
    games_won = db.Column(
        db.Integer, nullable=False, default=0, server_default=0
    )
    created_at = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
    last_modified = db.Column(
        db.DateTime, nullable=False,
        default=db.func.current_timestamp(),
        server_default=db.func.current_timestamp()
    )
