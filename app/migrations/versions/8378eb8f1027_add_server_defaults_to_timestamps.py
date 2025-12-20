"""Add server defaults to timestamps

Revision ID: 8378eb8f1027
Revises: 8b02360f4f69
Create Date: 2025-12-20 13:32:53.645936

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8378eb8f1027"
down_revision: Union[str, None] = "8b02360f4f69"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    for table in ("user", "listing", "wallet", "message", "favourite"):
        op.alter_column(
            table,
            "created_at",
            server_default=sa.func.now(),
            nullable=False,
        )
        op.alter_column(
            table,
            "updated_at",
            server_default=sa.func.now(),
            nullable=False,
        )


def downgrade():
    for table in ("user", "listing", "wallet", "message", "favourite"):
        op.alter_column(
            table,
            "created_at",
            server_default=None,
        )
        op.alter_column(
            table,
            "updated_at",
            server_default=None,
        )
