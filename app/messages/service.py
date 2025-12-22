from sqlalchemy import select, update

from app.core.database import async_session_maker
from app.messages.model import Message
from app.services.base import BaseService


class MessageService(BaseService):
    model = Message

    @classmethod
    async def send_message(cls, sender_id: int, data: dict):
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
