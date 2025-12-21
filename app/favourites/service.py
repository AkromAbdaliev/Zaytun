from sqlalchemy import select

from app.core.database import async_session_maker
from app.core.exceptions import FavouriteAlreadyExistsException
from app.favourites.model import Favourite
from app.listings.model import Listing
from app.services.base import BaseService
from app.users.model import User


class FavouriteService(BaseService):
    model = Favourite

    @classmethod
    async def get_favourite_listings(cls, current_user):
        async with async_session_maker() as session:
            query = (
                select(
                    Favourite.id.label("id"),
                    Favourite.listing_id,
                    Listing.user_id,
                    Listing.category_id,
                    Listing.location,
                    Listing.title,
                    Listing.is_active,
                    Listing.price,
                    Listing.description,
                )
                .join(Listing, Listing.id == Favourite.listing_id)
                .where(Favourite.user_id == current_user.id)
            )

            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def create_favourite_listing(cls, listing_id: int, user: User):
        existing_favourite = await cls.find_one_or_none(
            user_id=user.id, listing_id=listing_id
        )
        if existing_favourite:
            raise FavouriteAlreadyExistsException
        return await cls.add_one(user_id=user.id, listing_id=listing_id)
