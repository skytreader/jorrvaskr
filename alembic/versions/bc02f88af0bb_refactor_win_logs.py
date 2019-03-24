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
    op.rename_table("win_logs", "player_win_logs")


def downgrade():
    op.rename_table("player_win_logs", "win_logs")
