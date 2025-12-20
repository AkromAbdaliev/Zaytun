from app.listings.model import Listing
from app.services.base import BaseService


class ListingService(BaseService):
    model = Listing
