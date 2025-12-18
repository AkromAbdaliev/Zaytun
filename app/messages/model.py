from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func

from app.core.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    receiver_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    listing_id = Column(Integer, ForeignKey("listing.id"), index=True, nullable=True)
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
