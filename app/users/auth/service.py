from app.core.exceptions import UserAlreadyExistsException
from app.services.base import BaseService
from app.users.model import User
from app.users.schemas import SUserCreate
from app.users.security import get_password_hash


class AuthService(BaseService):
    model = User

    @classmethod
    async def register_user(cls, user_data: SUserCreate):
        existing_user = await cls.find_one_or_none(email=user_data.email)
        if existing_user:
            raise UserAlreadyExistsException

        user_dict = user_data.model_dump(
            exclude_unset=True, exclude={"password", "location"}
        )
        user_dict["hashed_password"] = get_password_hash(user_data.password)
        if user_data.location:
            user_dict["location"] = user_data.location.to_wkt()

        user = await cls.add_one(**user_dict)
        return user
