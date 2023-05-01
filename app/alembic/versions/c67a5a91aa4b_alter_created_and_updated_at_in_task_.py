"""alter_created_and_updated_at_in_task_table

Revision ID: c67a5a91aa4b
Revises: aea2e0b443bb
Create Date: 2023-04-27 15:49:54.361749

"""
from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c67a5a91aa4b"
down_revision = "aea2e0b443bb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "task",
        sa.Column(
            "created_at", sa.DateTime(), nullable=True, default=datetime.utcnow()
        ),
    )
    op.add_column(
        "task",
        sa.Column(
            "updated_at", sa.DateTime(), nullable=True, default=datetime.utcnow()
        ),
    )


def downgrade() -> None:
    op.drop_column("task", "created_at")
    op.drop_column("task", "updated_at")
