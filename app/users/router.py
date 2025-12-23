from fastapi import APIRouter, Depends, status

from app.core.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.users.schemas import SUserCreate, SUserRead, SUserUpdateForAdmin
from app.users.service import UserService
from app.users.dependencies import require_roles
from app.users.model import UserRole

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.get("", response_model=list[SUserRead])
async def get_users(current_admin=Depends(require_roles(UserRole.ADMIN))):
    return await UserService.find_all()


@router.get("/{user_id}", response_model=SUserRead)
async def get_user(
    user_id: int, current_admin=Depends(require_roles(UserRole.ADMIN))
):
    user = await UserService.find_by_id(user_id)
    if not user:
        raise UserNotFoundException
    return user


@router.post("", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: SUserCreate, current_admin=Depends(require_roles(UserRole.ADMIN))
):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    return await UserService.create_user(user_data)


@router.put(
    "/{user_id}", response_model=SUserRead, status_code=status.HTTP_202_ACCEPTED
)
async def update_user(
    user_id: int,
    user_data: SUserUpdateForAdmin,
    current_admin=Depends(require_roles(UserRole.ADMIN)),
):
    existing_user = await UserService.find_by_id(user_id)
    if not existing_user:
        raise UserNotFoundException
    return await UserService.update_user(existing_user, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, current_admin=Depends(require_roles(UserRole.ADMIN))
):
    existing_user = await UserService.find_by_id(user_id)
    if not existing_user:
        raise UserNotFoundException
    return await UserService.delete_one(existing_user)
