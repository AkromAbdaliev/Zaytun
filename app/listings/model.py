from geoalchemy2 import Geography
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func

from app.core.database import Base


class Listing(Base):
    __tablename__ = "listing"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id"), index=True, nullable=False)
    location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True)
    title = Column(String, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
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
