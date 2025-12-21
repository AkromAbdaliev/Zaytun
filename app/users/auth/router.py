from fastapi import APIRouter, Depends, Response, status

from app.core.exceptions import InvalidCredentialsException, UserAlreadyExistsException
from app.users.dependencies import authenticate_user, get_current_user
from app.users.schemas import SUserCreate, SUserLogin, SUserRead
from app.users.security import create_access_token, get_password_hash
from app.users.service import UserService

router = APIRouter(
    prefix="/auth",
    tags=["Authentications"],
)


@router.post("/register", response_model=SUserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserCreate):
    existing_user = await UserService.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    return await UserService.add_one(
        email=user_data.email, hashed_password=hashed_password
    )


@router.post("/login")
async def login_user(user_data: SUserLogin, response: Response):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise InvalidCredentialsException
    access_token = create_access_token(
        data={"sub": str(user.id), "email": str(user.email)}
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    response.delete_cookie(key="access_token")


@router.get("/me", response_model=SUserRead)
async def get_me(current_user=Depends(get_current_user)):
    return current_user
