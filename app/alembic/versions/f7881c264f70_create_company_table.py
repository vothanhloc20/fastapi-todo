"""create_company_table

Revision ID: f7881c264f70
Revises: c67a5a91aa4b
Create Date: 2023-04-28 03:08:10.274662

"""
import uuid
from datetime import datetime

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID

from app.models.data_enums import CompanyMode

# revision identifiers, used by Alembic.
revision = "f7881c264f70"
down_revision = "c67a5a91aa4b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    company_table = op.create_table(
        "company",
        sa.Column(
            "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
        ),
        sa.Column("name", sa.String, unique=True, nullable=False, index=True),
        sa.Column("description", sa.String, nullable=True),
        sa.Column(
            "mode", sa.Enum(CompanyMode), nullable=False, default=CompanyMode.Active
        ),
        sa.Column("rating", sa.SmallInteger, default=0),
        sa.Column(
            "created_at", sa.DateTime(), nullable=True, default=datetime.utcnow()
        ),
        sa.Column(
            "updated_at", sa.DateTime(), nullable=True, onupdate=datetime.utcnow()
        ),
    )

    op.bulk_insert(
        company_table,
        [
            {
                "id": uuid.uuid4(),
                "name": "ToDo Company",
                "description": "ToDo Company Description",
                "mode": CompanyMode.Active,
                "rating": 5,
            }
        ],
    )

    op.add_column(
        "user",
        sa.Column(
            "company_id", UUID(as_uuid=True), sa.ForeignKey("company.id"), nullable=True
        ),
    )


def downgrade() -> None:
    op.drop_table("company")
    op.drop_table("user", "company_id")
