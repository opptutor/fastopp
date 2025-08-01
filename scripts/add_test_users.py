# =========================
# add_test_users.py - Add test users to database
# =========================
import asyncio
from db import AsyncSessionLocal
from models import User
from fastapi_users.password import PasswordHelper


async def add_test_users():
    """Add test users to the database"""
    async with AsyncSessionLocal() as session:
        password_helper = PasswordHelper()
        password = "test123"
        hashed_pw = password_helper.hash(password)
        
        # Add several test users
        test_users = [
            {
                "email": "john@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False
            },
            {
                "email": "jane@example.com", 
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": False
            },
            {
                "email": "bob@example.com",
                "hashed_password": hashed_pw,
                "is_active": False,  # Inactive user
                "is_superuser": False
            },
            {
                "email": "admin2@example.com",
                "hashed_password": hashed_pw,
                "is_active": True,
                "is_superuser": True  # Another superuser
            }
        ]
        
        for user_data in test_users:
            user = User(**user_data)
            session.add(user)
        
        await session.commit()
        print("✅ Added test users to database!")
        print("Test users:")
        print("- john@example.com (active)")
        print("- jane@example.com (active)")
        print("- bob@example.com (inactive)")
        print("- admin2@example.com (superuser)")
        print("All users have password: test123")


if __name__ == "__main__":
    asyncio.run(add_test_users()) 