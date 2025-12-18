"""Add created_at and updated_at defaults to category

Revision ID: b0c87db0f82b
Revises: b08a7957acfd
Create Date: 2025-12-18 09:27:08.206413

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b0c87db0f82b"
down_revision: Union[str, None] = "b08a7957acfd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "category",
        "created_at",
        server_default=sa.func.now(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "category",
        "updated_at",
        server_default=sa.func.now(),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "category",
        "created_at",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
    op.alter_column(
        "category",
        "updated_at",
        server_default=None,
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False,
    )
