from fastapi import APIRouter, Depends, Response, status

from app.core.exceptions import InvalidCredentialsException
from app.users.auth.service import AuthService
from app.users.dependencies import authenticate_user, get_current_user
from app.users.schemas import SUserCreate, SUserLogin, SUserRead
from app.users.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentications"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserCreate, response: Response):
    user = await AuthService.register_user(user_data)

    access_token = create_access_token(
        data={"sub": str(user.id), "email": str(user.email)}
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token}


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
