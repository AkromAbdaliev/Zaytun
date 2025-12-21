from fastapi import APIRouter, Depends, status

from app.core.exceptions import FavouriteNotFoundException
from app.favourites.schemas import SFavouriteCreateResponse, SFavouriteRead
from app.favourites.service import FavouriteService
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/favourite",
    tags=["Favourites"],
)


@router.get("", response_model=list[SFavouriteRead])
async def get_favourites(current_user=Depends(get_current_user)):
    return await FavouriteService.get_favourite_listings(current_user)


@router.post(
    "",
    response_model=SFavouriteCreateResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_favourite(
    listing_id: int,
    current_user=Depends(get_current_user),
):
    return await FavouriteService.create_favourite_listing(listing_id, current_user)


@router.delete(
    "/{favourite_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_favourite(favourite_id: int):
    existing_favourite = await FavouriteService.find_by_id(favourite_id)
    if not existing_favourite:
        raise FavouriteNotFoundException
    return await FavouriteService.delete_one(existing_favourite)
