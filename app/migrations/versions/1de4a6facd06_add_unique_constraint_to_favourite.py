"""add unique constraint to favourite

Revision ID: 1de4a6facd06
Revises: 8378eb8f1027
Create Date: 2025-12-21 11:47:47.778199

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1de4a6facd06"
down_revision: Union[str, None] = "8378eb8f1027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make listing_id NOT NULL (if you want to fix that too)
    op.alter_column(
        "favourite", "listing_id", existing_type=sa.Integer(), nullable=False
    )

    # Add unique constraint (user_id + listing_id)
    op.create_unique_constraint(
        "uq_user_listing_favourite", "favourite", ["user_id", "listing_id"]
    )


def downgrade() -> None:
    # Drop the unique constraint
    op.drop_constraint("uq_user_listing_favourite", "favourite", type_="unique")

    # Revert listing_id to nullable
    op.alter_column(
        "favourite", "listing_id", existing_type=sa.Integer(), nullable=True
    )
