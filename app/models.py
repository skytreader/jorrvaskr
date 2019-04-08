from . import db
from datetime import datetime, timedelta
from sqlalchemy import column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

def get_or_create(model, session=None, will_commit=False, **kwargs):
    session = session if session else db.session
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)

        if will_commit:
            session.commit()
        else:
            session.flush()
        return instance

class GameType(db.Model):

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

    @staticmethod
    def get_gametype_from_label(label):
        gametype = GameType.query.filter_by(label=label).first()
        return gametype

    @staticmethod
    def get_label_by_id(_id):
        return GameType.query.filter_by(id=_id).first().label

class Player(db.Model):

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

class GameSession(db.Model):
    """
    One game session is one time people agree to play werewolf. In one game
    session, there may be multiple games of werewolf, each possibly with a
    different mix of possible game roles.
    """

    __tablename__ = "game_sessions"
    id = db.Column(db.Integer, primary_key=True)
    game_type_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "game_types.id", name="gamesession_gametype_fk1", ondelete="CASCADE"
        ),
        nullable=False
    )
    games_played = db.Column(
        db.Integer, nullable=False, default=0, server_default="0"
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

    game_type = relationship("GameType")

    @staticmethod
    def find_session(date, game_type_id):
        """
        Where date is a datetime object.
        """
        date_limit = date.date() + timedelta(days=1)
        return (
            db.session.query(GameSession)
            .filter(date <= GameSession.created_at)
            .filter(GameSession.created_at < date_limit)
            .order_by(GameSession.created_at)
            .first()
        )

class GameSessionRecord(db.Model):
    """
    For every game session, this table is a straight-up tally of a player's win-
    loss performance, **regardless of faction**.

    See also: FactionTally.
    """

    __tablename__ = "game_session_records"
    __table_args__ = (
        db.CheckConstraint(
            column("games_played") >= column("games_won"),
            name="gamesplayed_geq_gameswon_ck"
        ),
    )
    game_session_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "game_sessions.id", name="gamesessionrecord_gamesessions_fk1",
            ondelete="CASCADE"
        ), nullable=False, primary_key=True
    )
    player_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "players.id", name="gamesessionrecord_player_fk2",
            ondelete="CASCADE"
        ), nullable=False, primary_key=True
    )
    games_played = db.Column(
        db.Integer, nullable=False, default=0, server_default="0",
    )
    games_won = db.Column(
        db.Integer, nullable=False, default=0, server_default="0"
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

    game_session = relationship("GameSession")
    player = relationship("Player")

class Faction(db.Model):

    __tablename__ = "factions"
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

    @staticmethod
    def get_faction_from_name(faction_name):
        faction = Faction.query.filter_by(name=faction_name).first()
        return faction 

class FactionTally(db.Model):
    """
    This records the number of times a certain faction won. We don't record the
    number of times a certain faction was included in a game because in general,
    we don't care about that/we don't note that. We are not so concerned if some
    niche faction (e.g., Lovers, Cult, Masons) is included, only if they win.

    For each record, the game session is also stored. This could help in
    balancing the game based on outcome; the record can show a bias towards any
    one faction winning, based on the current mix of roles.

    (The following night, a mysterious group of individuals were seen lurking
    around the village. Everyone slept peacefully...only to wake up to the news
    of the macabre death of the programmer. Whoever did it left no clues except
    for the cryptic message "SILENCIO" written on the kitchen counter, beside
    some leftover soup stored in a mason jar.)

    See also: GameSessionRecord.
    """

    __tablename__ = "faction_tallies"
    faction_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "factions.id", name="factiontally_faction_fk1", ondelete="CASCADE"
        ), primary_key=True
    )
    game_session_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "game_sessions.id", name="factiontally_gamesession_fk2",
            ondelete="CASCADE"
        ), primary_key=True
    )
    games_won = db.Column(
        db.Integer, nullable=False, default=0, server_default="0"
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

    faction = relationship("Faction")
    game_session = relationship("GameSession")

class FactionWinLog(db.Model):
    __tablename__ = "faction_win_logs"
    id = db.Column(db.Integer, primary_key=True)
    game_session_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "game_sessions.id", name="factionwinlog_gamesessions_fk1",
            ondelete="CASCADE"
        ), nullable=False
    )
    faction_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "factions.id", name="factionwinlog_factions_fk2",
            ondelete="CASCADE"
        ), nullable=False
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

    game_session = relationship("GameSession")
    faction = relationship("Faction")

class PlayerWinLog(db.Model):
    """
    A slightly more detailed record of wins. One win for one player is one, and
    only one, row in this table.

    Note that this might not fully coincide with the game session records. This
    is because in our original tracking, such detailed information was not kept.
    """

    __tablename__ = "player_win_logs"
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "players.id", name="winlog_player_fk1", ondelete="CASCADE"
        ), nullable=False
    )
    # This is nullable because in the future we want to import player win log
    # data from sources which might not have been as stringent as this data
    # model in keeping track of things (*ahem*spreadsheet*ahem*).
    faction_win_log_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "faction_win_logs.id",
            name="playerwinlog_factionwinlog_fk2",
            ondelete="CASCADE"
        ),
        nullable=True
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

    player = relationship("Player")
    faction_win_log = relationship("FactionWinLog")

class WinWeight(db.Model):

    __tablename__ = "win_weights"
    faction_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "factions.id", name="winweight_factions_fk3",
            ondelete="CASCADE"
        ), primary_key=True
    )
    weight = db.Column(
        db.Float, nullable=False, default=0.0, server_default="0.0"
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

    faction = relationship("Faction")
