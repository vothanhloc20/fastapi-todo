"""create_user_table

Revision ID: 9449c3b72bba
Revises:
Create Date: 2023-04-27 10:50:38.843550

"""
import uuid
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

from app.services.auth_service import AuthService
from app.settings import settings

# revision identifiers, used by Alembic.
revision = "9449c3b72bba"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    user_table = op.create_table(
        "user",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
        ),
        sa.Column("email", sa.String, unique=True, nullable=False, index=True),
        sa.Column("username", sa.String, unique=True, nullable=False, index=True),
        sa.Column("first_name", sa.String, nullable=True),
        sa.Column("last_name", sa.String, nullable=True),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, default=False),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column(
            "created_at", sa.DateTime(), nullable=True, default=datetime.utcnow()
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=True, onupdate=datetime.utcnow()
        ),
    )

    op.bulk_insert(
        user_table,
        [
            {
                "id": uuid.uuid4(),
                "email": "admin@admin.com",
                "username": "admin",
                "first_name": "App",
                "last_name": "Admin",
                "hashed_password": AuthService().get_password_hash(
                    settings.ADMIN_DEFAULT_PASSWORD
                ),
                "is_active": True,
                "is_admin": True,
            }
        ],
    )


def downgrade() -> None:
    op.drop_table("user")
