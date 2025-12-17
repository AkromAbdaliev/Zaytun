from fastapi import APIRouter, status

from app.users.schemas import SUserCreate, SUserRead
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


@router.put("/{user_id}")
async def update_user(user_id: int):
    return {"message": f"User {user_id} updated"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}
