from fastapi import APIRouter, status

from app.core.exceptions import ListingNotFoundException
from app.listings.schemas import SListingCreate, SListingRead, SListingUpdate
from app.listings.service import ListingService

router = APIRouter(
    prefix="/listing",
    tags=["Listing"],
)


@router.get("", response_model=list[SListingRead])
async def get_listings():
    return await ListingService.find_all_active()


@router.get("/{listing_id}", response_model=SListingRead)
async def get_listing(listing_id: int):
    existing_listing = await ListingService.find_by_id(listing_id)
    if not existing_listing:
        raise ListingNotFoundException
    return existing_listing


@router.post(
    "",
    response_model=SListingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_listing(listing_data: SListingCreate):
    return await ListingService.create_listing(listing_data)


@router.put(
    "/{listing_id}",
    response_model=SListingRead,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_listing(listing_id: int, listing_data: SListingUpdate):
    existing_listing = await ListingService.find_by_id(listing_id)
    if not existing_listing:
        raise ListingNotFoundException
    return await ListingService.update_listing(existing_listing, listing_data)


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_listing(listing_id: int):
    existing_listing = await ListingService.find_by_id(listing_id)
    if not existing_listing:
        raise ListingNotFoundException
    return await ListingService.delete_one(existing_listing)
