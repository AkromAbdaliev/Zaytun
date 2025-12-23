"""add user role column

Revision ID: c2c0a7a1af3c
Revises: 242fd8c2427d
Create Date: 2025-12-23 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "c2c0a7a1af3c"
down_revision = "242fd8c2427d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Step 1: Create the ENUM type
    user_role_enum = postgresql.ENUM(
        "user", "admin", name="user_role", create_type=True
    )
    user_role_enum.create(op.get_bind())

    # Step 2: Add the column using the enum
    op.add_column(
        "user", sa.Column("role", user_role_enum, nullable=False, server_default="user")
    )


def downgrade() -> None:
    # Drop the column first
    op.drop_column("user", "role")

    # Then drop the ENUM type
    user_role_enum = postgresql.ENUM(name="user_role")
    user_role_enum.drop(op.get_bind())
