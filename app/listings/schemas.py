from pydantic import BaseModel

from app.core.schemas import Geopoint


class SListingCreate(BaseModel):
    user_id: int
    category_id: int
    location: Geopoint | None = None  # WKT representation of the location
    title: str
    price: int
    description: str | None = None


class SListingRead(BaseModel):
    id: int
    user_id: int
    category_id: int
    location: Geopoint | None = None  # WKT representation of the location
    title: str
    is_active: bool
    price: int
    description: str | None = None
