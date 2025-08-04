# =========================
# admin_auth.py - SQLAdmin authentication
# =========================
from typing import Optional
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from sqlalchemy import select
from db import AsyncSessionLocal
from models import User
from fastapi_users.password import PasswordHelper


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Handle admin login with database verification"""
        form = await request.form()
        username = form.get("username", "")
        password = form.get("password", "")
        
        # Ensure password is a string
        if isinstance(password, str):
            password_str = password
        else:
            # Handle case where password might be UploadFile or other type
            password_str = str(password)
        
        # Verify user against database
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User).where(User.email == username)  # type: ignore
            )
            user: Optional[User] = result.scalar_one_or_none()  # type: ignore
            
            if not user:
                return False
            
            # Verify password using FastAPI Users password helper
            password_helper = PasswordHelper()
            if not password_helper.verify_and_update(password_str, user.hashed_password):  # type: ignore
                return False
            
            # Check if user is active and has admin access (superuser OR staff)
            if not user.is_active or not (user.is_superuser or user.is_staff):  # type: ignore
                return False
            
            # Store user info in session with group and permissions
            request.session.update({
                "admin": True,
                "user_id": str(user.id),  # type: ignore
                "user_email": user.email,  # type: ignore
                "is_superuser": user.is_superuser,  # type: ignore
                "is_staff": user.is_staff,  # type: ignore
                "group": user.group,  # type: ignore
                "can_manage_webinars": user.is_superuser or user.group in ["marketing", "sales"]  # type: ignore
            })
            return True

    async def logout(self, request: Request) -> bool:
        """Handle admin logout"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated"""
        return request.session.get("admin", False) 