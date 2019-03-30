"""refactor win logs

Revision ID: bc02f88af0bb
Revises: 1fe94d2a6ef1
Create Date: 2019-03-24 19:55:03.429092

"""
from alembic import op
from datetime import datetime
from sqlalchemy.sql import bindparam, distinct, select
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc02f88af0bb'
down_revision = '1fe94d2a6ef1'
branch_labels = None
depends_on = None


def upgrade():
    now = datetime.now()
    conn = op.get_bind()
    metadata = sa.MetaData(bind=conn)
    win_logs_table = sa.Table("win_logs", metadata, autoload=True)

    # Get the contents of faction_win_logs from win_logs
    # Only works because right now we are sure that win_logs has so few records.
    # In actuality, should block this transaction.
    derived_faction_wins = conn.execute(
        select([distinct((
            win_logs_table.c.game_session_id,
            win_logs_table.c.faction_id,
            win_logs_table.c.created_at
        ))])
    )
    faction_win_logs_table = op.create_table(
        "faction_win_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "game_session_id",
            sa.Integer,
            sa.ForeignKey(
                "game_sessions.id", name="factionwinlog_gamesessions_fk1",
                ondelete="CASCADE"
            ),
            nullable=False
        ),
        sa.Column(
            "faction_id",
            sa.Integer,
            sa.ForeignKey(
                "factions.id", name="factionwinlog_factions_fk2", ondelete="CASCADE"
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

    for faction_win, in derived_faction_wins:
        conn.execute(
            faction_win_logs_table.insert(),
            game_session_id=faction_win[0],
            faction_id=faction_win[1],
            created_at=faction_win[2],
            updated_at=now
        )

    op.drop_column("win_logs", "game_session_id")
    op.drop_column("win_logs", "faction_id")
    op.add_column(
        "win_logs",
        sa.Column(
            "faction_win_log_id",
            sa.Integer,
            sa.ForeignKey(
                "faction_win_logs.id",
                name="playerwinlog_factionwinlog_fk2", 
                ondelete="CASCADE"
            ),
            nullable=True
        )
    )
    op.rename_table("win_logs", "player_win_logs")


def downgrade():
    conn = op.get_bind()
    metadata = sa.MetaData(bind=conn)
    op.rename_table("player_win_logs", "win_logs")

    # win_logs will be left in an inconsistent state for the meantime.
    op.add_column(
        "win_logs",
        sa.Column(
            "faction_id",
            sa.Integer,
            sa.ForeignKey(
                "factions.id", name="winlog_factions_fk3", ondelete="CASCADE"
            ),
            nullable=False
        )
    )
    op.add_column(
        "win_logs",
        sa.Integer,
        sa.Column(
            "game_session_id",
            sa.Integer,
            sa.ForeignKey(
                "game_sessions.id", name="winlog_gamesessions_fk2",
                ondelete="CASCADE"
            ),
            nullable=False
        )
    )
    
    faction_wins_table = sa.Table("faction_wins", metadata, autoload=True)
    win_logs_table = sa.Table("win_logs", metadata, autoload=True)

    # This assumes that the tuple (game_session_id, faction_id, created_at) is a
    # unique. While the DB does not enforce this constraint, this actually
    # reflects the state of the data. If a bunch of super-fact werewolf-playing
    # AI agents were to store stats in Jorrvaskr, this assumption might not hold.
    faction_win_records = conn.execute(
        select([
            faction_wins_table.c.id,
            faction_wins_table.c.game_session_id,
            faction_wins_table.c.faction_id,
            faction_wins_table.c.created_at
        ])
    )

    for win_record in faction_win_records:
        params = {
            "b_faction_win_id": win_record[0],
            "b_game_session_id": win_record[1],
            "b_faction_id": win_record[2],
            "b_created_at": win_record[3],
        }
        conn.execute(
            win_logs_table.update()
            .where(table.c.faction_win_log_id == bindparam("b_faction_win_id"))
            .values(
                faction_id=bindparam("b_faction_id"),
                game_session_id=bindparam("b_game_session_id"),
                created_at=bindparam("b_created_at")
            )
        )

    op.drop_column("win_logs", "faction_win_log_id")
    op.drop_table("faction_win_logs")
