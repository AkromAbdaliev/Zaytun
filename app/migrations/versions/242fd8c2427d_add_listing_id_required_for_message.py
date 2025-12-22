"""add listing id required for message

Revision ID: 242fd8c2427d
Revises: 1de4a6facd06
Create Date: 2025-12-21 17:13:08.714824

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "242fd8c2427d"
down_revision: Union[str, None] = "1de4a6facd06"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "message",
        "listing_id",
        existing_type=sa.Integer(),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "message",
        "listing_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
