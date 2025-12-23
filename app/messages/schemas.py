from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SMessageCreate(BaseModel):
    receiver_id: int
    listing_id: int
    content: str


class SMessageRead(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    listing_id: int
    content: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
