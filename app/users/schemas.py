from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from app.core.schemas import Geopoint
from app.users.model import UserRole


class SUserCreate(BaseModel):
    email: EmailStr
    password: str
    phone: str | None = None
    location: Geopoint | None = None  # WKT representation of the location
    username: str | None = None


class SUserRead(BaseModel):
    id: int
    email: EmailStr
    phone: str | None = None
    location: Geopoint | None = None  # WKT representation of the location
    username: str | None = None
    is_verified: bool
    is_active: bool
    role: UserRole
    model_config = ConfigDict(from_attributes=True)

    @field_validator("location", mode="before")
    def wkb_to_geopoint(cls, value):
        if value is None:
            return None
        return Geopoint.from_wkb(value)


class SUserUpdateForUser(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    location: Geopoint | None = None  # WKT representation of the location
    username: str | None = None


class SUserChangePassword(BaseModel):
    old_password: str
    new_password: str


class SUserUpdateForAdmin(BaseModel):
    email: EmailStr | None = None
    phone: str | None = None
    location: Geopoint | None = None  # WKT representation of the location
    username: str | None = None
    is_verified: bool | None = None
    is_active: bool | None = None
    role: UserRole | None = None


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
