# =========================
# init_db.py - Database initialization script
# =========================
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from db import DATABASE_URL
from models import Base


async def init_db():
    """Initialize the database by creating all tables."""
    engine = create_async_engine(DATABASE_URL, echo=True)

    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
