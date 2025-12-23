import enum

from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=True)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    username = Column(String, nullable=True, default=None)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    role = Column(
        Enum(UserRole, name="user_role"),
        nullable=False,
        server_default=UserRole.USER.value,
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationships with passive_deletes=True (relies on DB cascade)
    listings = relationship("Listing", back_populates="user", passive_deletes=True)
    wallets = relationship("Wallet", back_populates="user", passive_deletes=True)
    sent_messages = relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        passive_deletes=True,
    )
    received_messages = relationship(
        "Message",
        foreign_keys="Message.receiver_id",
        back_populates="receiver",
        passive_deletes=True,
    )
