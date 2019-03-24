"""initial db tables

Revision ID: 1fe94d2a6ef1
Revises: 
Create Date: 2019-03-14 17:22:29.685536

"""
from alembic import op
from sqlalchemy.engine.reflection import Inspector
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fe94d2a6ef1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    not_exists = lambda tbl: tbl not in tables

    if not_exists("game_types"):
        op.create_table(
            "game_types",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("label", sa.String, nullable=False, unique=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("players"):
        op.create_table(
            "players",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("name", sa.String, nullable=False, unique=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("game_sessions"):
        op.create_table(
            "game_sessions",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column(
                "game_type_id", sa.Integer,
                sa.ForeignKey(
                    "game_types.id",
                    name="gamesession_gametype_fk1",
                    ondelete="CASCADE"
                ),
                nullable=False
            ),
            sa.Column(
                "games_played", sa.Integer, nullable=False, default=0,
                server_default="0"
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("game_session_records"):
        op.create_table(
            "game_session_records",
            sa.Column(
                "game_session_id", sa.Integer,
                sa.ForeignKey(
                    "game_sessions.id",
                    name="gamesessionrecord_gamesessions_fk1",
                    ondelete="CASCADE"
                ),
                nullable=False, primary_key=True
            ),
            sa.Column(
                "player_id", sa.Integer,
                sa.ForeignKey(
                    "players.id",
                    name="gamesessionrecord_player_fk2",
                    ondelete="CASCADE"
                ),
                nullable=False, primary_key=True
            ),
            sa.Column(
                "games_played", sa.Integer, nullable=False, default=0,
                server_default="0"
            ),
            sa.Column(
                "games_won", sa.Integer, nullable=False, default=0,
                server_default="0"
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("factions"):
        op.create_table(
            "factions",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column("name", sa.String, nullable=False, unique=True),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("faction_tallies"):
        op.create_table(
            "faction_tallies",
            sa.Column(
                "faction_id", sa.Integer,
                sa.ForeignKey(
                    "factions.id", name="factiontally_faction_fk1",
                    ondelete="CASCADE",
                ),
                primary_key=True
            ),
            sa.Column(
                "game_sessions.id",
                sa.ForeignKey(
                    "game_sessions.id", name="factiontally_gamesession_fk2",
                    ondelete="CASCADE"
                ),
                primary_key=True
            ),
            sa.Column(
                "games_won", sa.Integer, nullable=False, default=0,
                server_default="0"
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("win_logs"):
        op.create_table(
            "win_logs",
            sa.Column("id", sa.Integer, primary_key=True),
            sa.Column(
                "player_id",
                sa.Integer,
                sa.ForeignKey(
                    "players.id", name="winlog_player_fk1", ondelete="CASCADE"
                ),
                nullable=False
            ),
            sa.Column(
                "game_session_id",
                sa.Integer,
                sa.ForeignKey(
                    "game_sessions.id", name="winlog_gamesessions_fk2",
                    ondelete="CASCADE"
                ),
                nullable=False
            ),
            sa.Column(
                "faction_id",
                sa.ForeignKey(
                    "factions.id", name="winlog_factions_fk3", ondelete="CASCADE"
                ),
                nullable=False
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )
    if not_exists("win_weights"):
        op.create_table(
            "win_weights",
            sa.Column(
                "faction_id", sa.Integer,
                sa.ForeignKey(
                    "factions.id", name="winweight_factions_fk3", ondelete="CASCADE"
                ),
                primary_key=True
            ),
            sa.Column(
                "weight", sa.Float, nullable=False, default=0.0,
                server_default="0.0"
            ),
            sa.Column(
                "created_at", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            ),
            sa.Column(
                "last_modified", sa.DateTime, nullable=False,
                server_default=sa.func.current_timestamp()
            )
        )


def downgrade():
    op.drop_table("game_type")
    op.drop_table("players")
    op.drop_table("game_sessions")
    op.drop_table("game_session_records")
    op.drop_table("factions")
    op.drop_table("faction_tallies")
    op.drop_table("win_logs")
    op.drop_table("win_weights")
