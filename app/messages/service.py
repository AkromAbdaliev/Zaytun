from sqlalchemy import and_, or_, select, update

from app.core.exceptions import ForbiddenException, ListingNotFoundException
from app.core.database import async_session_maker
from app.listings.service import ListingService
from app.messages.model import Message
from app.services.base import BaseService


class MessageService(BaseService):
    model = Message

    @classmethod
    async def send_message(cls, sender_id: int, data: dict):
        listing = await ListingService.find_by_id(data["listing_id"])
        if not listing:
            raise ListingNotFoundException

        receiver_id = data["receiver_id"]
        if receiver_id == sender_id:
            raise ForbiddenException

        if listing.user_id not in (sender_id, receiver_id):
            raise ForbiddenException

        return await cls.add_one(sender_id=sender_id, **data)

    @classmethod
    async def get_inbox(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(Message)
                .where(Message.receiver_id == user_id)
                .order_by(Message.created_at.desc())
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def get_thread(
        cls, user_id: int, other_user_id: int, listing_id: int
    ):
        listing = await ListingService.find_by_id(listing_id)
        if not listing:
            raise ListingNotFoundException

        if listing.user_id not in (user_id, other_user_id):
            raise ForbiddenException

        async with async_session_maker() as session:
            query = (
                select(Message)
                .where(
                    Message.listing_id == listing_id,
                    or_(
                        and_(
                            Message.sender_id == user_id,
                            Message.receiver_id == other_user_id,
                        ),
                        and_(
                            Message.sender_id == other_user_id,
                            Message.receiver_id == user_id,
                        ),
                    ),
                )
                .order_by(Message.created_at.asc())
            )
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def mark_as_read(cls, message_id: int, user_id: int):
        async with async_session_maker() as session:
            query = (
                update(Message)
                .where(
                    Message.id == message_id,
                    Message.receiver_id == user_id,
                )
                .values(is_read=True)
                .returning(Message)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
