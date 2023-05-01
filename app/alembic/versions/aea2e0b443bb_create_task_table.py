"""create_task_table

Revision ID: aea2e0b443bb
Revises: 9449c3b72bba
Create Date: 2023-04-27 14:22:00.918127

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

from app.models.data_enums import TaskPriority, TaskStatus

# revision identifiers, used by Alembic.
revision = "aea2e0b443bb"
down_revision = "9449c3b72bba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "task",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
        ),
        sa.Column("summary", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=True),
        sa.Column(
            "status", sa.Enum(TaskStatus), nullable=False, default=TaskStatus.NotStarted
        ),
        sa.Column("priority", sa.Enum(TaskPriority), nullable=True),
        sa.Column(
            "user_id", UUID(as_uuid=True), sa.ForeignKey("user.id"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_table("task")
