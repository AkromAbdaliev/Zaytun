from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    images = Column(String, nullable=True)
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

    subcategories = relationship("Category", backref="parent", remote_side=[id])
