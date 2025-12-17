from sqlalchemy.exc import IntegrityError

from app.core.exceptions import UserAlreadyExistsException
from app.services.base import BaseService
from app.users.auth import get_password_hash
from app.users.model import User
from app.users.schemas import SUserCreate, SUserUpdateForUser


class UserService(BaseService):
    model = User

    @classmethod
    async def create_user(cls, user_create: SUserCreate) -> User:
        data = user_create.model_dump(
            exclude_unset=True, exclude={"password", "location"}
        )
        data["hashed_password"] = get_password_hash(user_create.password)
        if user_create.location:
            data["location"] = user_create.location.to_wkt()

        try:
            return await cls.add_one(**data)
        except IntegrityError:
            raise UserAlreadyExistsException

    @classmethod
    async def update_user(
        cls,
        user: User,
        data_in: SUserUpdateForUser,
    ) -> User:

        data = data_in.model_dump(
            exclude_unset=True,
            exclude={"location"},
        )

        if data_in.location:
            data["location"] = data_in.location.to_wkt()

        try:
            return await cls.update_one(user, **data)
        except IntegrityError:
            raise UserAlreadyExistsException
