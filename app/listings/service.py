from app.listings.model import Listing
from app.listings.schemas import SListingCreate
from app.services.base import BaseService


class ListingService(BaseService):
    model = Listing

    @classmethod
    async def create_listing(cls, listing_create: SListingCreate) -> Listing:
        data = listing_create.model_dump(
            exclude_unset=True,
            exclude={"location"},
        )
        return await cls.add_one(**data)
