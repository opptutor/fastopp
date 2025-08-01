import asyncio
from sqlalchemy import insert
from db import AsyncSessionLocal
from models import User
from fastapi_users.password import PasswordHelper


async def create_superuser():
    async with AsyncSessionLocal() as session:
        password_helper = PasswordHelper()
        password = "admin123"
        hashed_pw = password_helper.hash(password)
        stmt = insert(User).values(
            email="admin@example.com",
            hashed_password=hashed_pw,
            is_active=True,
            is_superuser=True
        )
        await session.execute(stmt)
        await session.commit()
        print("✅ Superuser created: admin@example.com / admin123")

if __name__ == "__main__":
    asyncio.run(create_superuser())
