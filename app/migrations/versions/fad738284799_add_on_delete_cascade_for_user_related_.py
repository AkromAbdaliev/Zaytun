"""add on delete cascade for user related tables

Revision ID: fad738284799
Revises: c2c0a7a1af3c
Create Date: 2025-12-23 15:59:48.574516

"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fad738284799"
down_revision: Union[str, None] = "c2c0a7a1af3c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Listing.user_id → user.id
    op.drop_constraint("listing_user_id_fkey", "listing", type_="foreignkey")
    op.create_foreign_key(
        "listing_user_id_fkey",
        "listing",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Wallet.user_id → user.id
    op.drop_constraint("wallet_user_id_fkey", "wallet", type_="foreignkey")
    op.create_foreign_key(
        "wallet_user_id_fkey", "wallet", "user", ["user_id"], ["id"], ondelete="CASCADE"
    )

    # Message.sender_id → user.id
    op.drop_constraint("message_sender_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        "message_sender_id_fkey",
        "message",
        "user",
        ["sender_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Message.receiver_id → user.id
    op.drop_constraint("message_receiver_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        "message_receiver_id_fkey",
        "message",
        "user",
        ["receiver_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Bonus: Message.listing_id → listing.id (clean up messages when listing is deleted)
    op.drop_constraint("message_listing_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        "message_listing_id_fkey",
        "message",
        "listing",
        ["listing_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    # Revert to NO ACTION / RESTRICT (default PostgreSQL behavior)

    # Listing.user_id
    op.drop_constraint("listing_user_id_fkey", "listing", type_="foreignkey")
    op.create_foreign_key(
        "listing_user_id_fkey", "listing", "user", ["user_id"], ["id"]
    )

    # Wallet.user_id
    op.drop_constraint("wallet_user_id_fkey", "wallet", type_="foreignkey")
    op.create_foreign_key("wallet_user_id_fkey", "wallet", "user", ["user_id"], ["id"])

    # Message.sender_id
    op.drop_constraint("message_sender_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        "message_sender_id_fkey", "message", "user", ["sender_id"], ["id"]
    )

    # Message.receiver_id
    op.drop_constraint("message_receiver_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        "message_receiver_id_fkey", "message", "user", ["receiver_id"], ["id"]
    )

    # Message.listing_id
    op.drop_constraint("message_listing_id_fkey", "message", type_="foreignkey")
    op.create_foreign_key(
        "message_listing_id_fkey", "message", "listing", ["listing_id"], ["id"]
    )
