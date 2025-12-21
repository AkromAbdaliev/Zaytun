from pydantic import BaseModel, ConfigDict

from app.core.schemas import Geopoint


class SFavouriteRead(BaseModel):
    id: int
    listing_id: int
    user_id: int
    category_id: int
    location: Geopoint | None = None  # WKT representation of the location
    title: str
    is_active: bool
    price: int
    description: str | None = None
    model_config = ConfigDict(from_attributes=True)


class SFavouriteCreateResponse(BaseModel):
    id: int
    listing_id: int
    model_config = ConfigDict(from_attributes=True)
