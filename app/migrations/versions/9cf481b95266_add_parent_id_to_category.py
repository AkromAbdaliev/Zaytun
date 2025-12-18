"""Add parent_id to category

Revision ID: 9cf481b95266
Revises: a3d676930188
Create Date: 2025-12-18 08:48:48.682512

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9cf481b95266"
down_revision: Union[str, None] = "a3d676930188"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add parent_id column
    op.add_column("category", sa.Column("parent_id", sa.Integer(), nullable=True))
    # Add self-referential foreign key
    op.create_foreign_key(
        "fk_category_parent", "category", "category", ["parent_id"], ["id"]
    )


def downgrade() -> None:
    # Drop foreign key
    op.drop_constraint("fk_category_parent", "category", type_="foreignkey")
    # Drop column
    op.drop_column("category", "parent_id")
