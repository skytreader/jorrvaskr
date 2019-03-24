"""refactor win logs

Revision ID: bc02f88af0bb
Revises: 1fe94d2a6ef1
Create Date: 2019-03-24 19:55:03.429092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc02f88af0bb'
down_revision = '1fe94d2a6ef1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "faction_win_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "game_session_id",
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
    op.rename_table("win_logs", "player_win_logs")


def downgrade():
    op.rename_table("player_win_logs", "win_logs")
