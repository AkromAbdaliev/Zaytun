from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False
    )
    receiver_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), index=True, nullable=False
    )
    listing_id = Column(
        Integer,
        ForeignKey("listing.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    content = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
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

    # Optional: Add relationships for ORM convenience
    sender = relationship(
        "User", foreign_keys=[sender_id], back_populates="sent_messages"
    )
    receiver = relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_messages"
    )
    listing = relationship("Listing", back_populates="messages")
