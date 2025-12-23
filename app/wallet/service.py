from sqlalchemy import select, update

from app.core.database import async_session_maker
from app.core.exceptions import InsufficientBalanceException
from app.services.base import BaseService
from app.wallet.model import Wallet


class WalletService(BaseService):
    model = Wallet

    @classmethod
    async def get_or_create_wallet(cls, user_id: int) -> Wallet:
        async with async_session_maker() as session:
            query = select(Wallet).where(Wallet.user_id == user_id)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()
            if wallet:
                return wallet

            insert_stmt = (
                Wallet.__table__.insert()
                .values(user_id=user_id, balance=0)
                .returning(Wallet)
            )
            result = await session.execute(insert_stmt)
            wallet = result.scalar_one()
            await session.commit()
            return wallet

    @classmethod
    async def top_up(cls, user_id: int, amount: int) -> Wallet:
        async with async_session_maker() as session:
            query = select(Wallet).where(Wallet.user_id == user_id)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()
            if not wallet:
                insert_stmt = (
                    Wallet.__table__
                    .insert()
                    .values(user_id=user_id, balance=amount)
                    .returning(Wallet)
                )
                result = await session.execute(insert_stmt)
                wallet = result.scalar_one()
                await session.commit()
                return wallet

            stmt = (
                update(Wallet)
                .where(Wallet.id == wallet.id)
                .values(balance=Wallet.balance + amount)
                .returning(Wallet)
            )
            result = await session.execute(stmt)
            updated_wallet = result.scalar_one()
            await session.commit()
            return updated_wallet

    @classmethod
    async def spend(cls, user_id: int, amount: int) -> Wallet:
        async with async_session_maker() as session:
            query = select(Wallet).where(Wallet.user_id == user_id)
            result = await session.execute(query)
            wallet = result.scalar_one_or_none()
            if not wallet or wallet.balance < amount:
                raise InsufficientBalanceException

            stmt = (
                update(Wallet)
                .where(Wallet.id == wallet.id)
                .values(balance=Wallet.balance - amount)
                .returning(Wallet)
            )
            result = await session.execute(stmt)
            updated_wallet = result.scalar_one()
            await session.commit()
            return updated_wallet


