from app.listings.model import Listing
from app.listings.schemas import SListingCreate, SListingUpdate
from app.services.base import BaseService


class ListingService(BaseService):
    model = Listing

    @classmethod
    async def find_all_active(cls):
        return await cls.find_all(is_active=True)

    @classmethod
    async def create_listing(cls, listing_create: SListingCreate) -> Listing:
        data = listing_create.model_dump(
            exclude_unset=True,
            exclude={"location"},
        )
        if listing_create.location:
            data["location"] = listing_create.location.to_wkt()
        return await cls.add_one(**data)

    @classmethod
    async def update_listing(
        cls,
        existing_listing: Listing,
        listing_update: SListingUpdate,
    ) -> Listing:
        data = listing_update.model_dump(
            exclude_unset=True,
            exclude={"location"},
        )
        if listing_update.location:
            data["location"] = listing_update.location.to_wkt()
        return await cls.update_one(existing_listing, **data)
