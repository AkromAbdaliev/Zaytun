import asyncio

import asyncpg

from app.core.config import settings


async def test_connection():
    dsn = settings.DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
    try:
        conn = await asyncpg.connect(dsn)
        await conn.close()
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_connection())
