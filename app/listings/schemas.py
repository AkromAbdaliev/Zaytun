from pydantic import BaseModel, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)


class SListingUpdate(BaseModel):
    category_id: int | None = None
    location: Geopoint | None = None
    title: str | None = None
    price: int | None = None
    description: str | None = None
