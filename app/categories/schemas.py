from pydantic import BaseModel, ConfigDict


class SCategoryRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    images: str | None = None
    model_config = ConfigDict(from_attributes=True)


class SCategoryCreate(BaseModel):
    name: str
    description: str | None = None
    images: str | None = None
