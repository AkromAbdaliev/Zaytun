from sqlalchemy import Column, DateTime, ForeignKey, Integer, func

from app.core.database import Base


class Favourite(Base):
    __tablename__ = "favourite"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    listing_id = Column(Integer, ForeignKey("listing.id"), index=True, nullable=True)
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
