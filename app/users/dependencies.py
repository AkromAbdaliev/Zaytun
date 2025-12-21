from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt
from pydantic import EmailStr

from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenFormatException,
    TokenExpiredException,
    UnauthorizedException,
    UserNotFoundException,
)
from app.users.model import User
from app.users.security import verify_password
from app.users.service import UserService


def get_token(reuquest: Request):
    access_token = reuquest.cookies.get("access_token")
    if not access_token:
        raise UnauthorizedException
    return reuquest.cookies.get("access_token")


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise InvalidTokenFormatException
    user_id: str = payload.get("sub")
    if user_id is None:
        raise InvalidTokenFormatException
    email: str = payload.get("email")
    if email is None:
        raise InvalidTokenFormatException
    expire: int = payload.get("exp")
    if expire is None or expire < datetime.now(timezone.utc).timestamp():
        raise TokenExpiredException

    user = await UserService.find_one_or_none(id=int(user_id))
    if user is None:
        raise UserNotFoundException
    return user


async def authenticate_user(email: EmailStr, password: str) -> User:
    user = await UserService.find_one_or_none(email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user
