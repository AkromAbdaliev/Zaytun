from fastapi import APIRouter, status

from app.core.exceptions import UserNotFoundException
from app.users.schemas import SUserCreate, SUserRead, SUserUpdateForUser
from app.users.service import UserService

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("", response_model=list[SUserRead])
async def get_users():
    users = await UserService.find_all()
    return [SUserRead.model_validate(user) for user in users]


@router.get("/{user_id}")
async def get_user(user_id: int):
    user = await UserService.find_by_id(user_id)
    return SUserRead.model_validate(user)


@router.post("", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: SUserCreate):
    new_user = await UserService.create_user(user_data)
    return SUserRead.model_validate(new_user)


@router.put("/{user_id}", response_model=SUserRead)
async def update_user(
    user_id: int,
    user_data: SUserUpdateForUser,
):
    user = await UserService.find_by_id(user_id)
    if not user:
        raise UserNotFoundException

    return await UserService.update_user(user, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    existing_user = await UserService.find_by_id(user_id)
    if not existing_user:
        raise UserNotFoundException
    await UserService.delete_one(existing_user)
    return
