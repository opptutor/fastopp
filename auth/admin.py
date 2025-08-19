# =========================
# auth/admin.py - SQLAdmin authentication
# =========================
from typing import Optional
from datetime import datetime
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
            import uuid
            session_id = str(uuid.uuid4())
            request.session.update({
                "admin": True,
                "user_id": str(user.id),  # type: ignore
                "user_email": user.email,  # type: ignore
                "is_superuser": user.is_superuser,  # type: ignore
                "is_staff": user.is_staff,  # type: ignore
                "group": user.group,  # type: ignore
                "can_manage_webinars": user.is_superuser or user.group in ["marketing", "sales"],  # type: ignore
                "login_time": datetime.now().isoformat(),
                "expires": 3600,  # 1 hour from now (in seconds)
                "session_id": session_id,  # Unique session identifier
                "logged_out": False  # Track logout status
            })
            return True

    async def logout(self, request: Request) -> bool:
        """Handle admin logout with comprehensive session cleanup"""
        try:
            # Clear all session data
            request.session.clear()
            
            # Force session expiration by setting a past timestamp
            request.session["expires"] = 0
            
            # Clear any remaining session keys
            for key in list(request.session.keys()):
                del request.session[key]
                
            # Set a logout timestamp to track logout events
            request.session["logout_time"] = datetime.now().isoformat()
            request.session["logged_out"] = True
            
            # Invalidate the session ID to prevent reuse
            if "session_id" in request.session:
                request.session["session_id"] = "INVALIDATED_" + request.session["session_id"]
                
            return True
        except Exception as e:
            print(f"Warning: Error during logout: {e}")
            # Even if there's an error, try to clear the session
            try:
                request.session.clear()
            except Exception:
                pass
            return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated with session expiration and logout tracking"""
        # Check if user has been logged out
        if request.session.get("logged_out", False):
            request.session.clear()
            return False
        
        # Check if session ID has been invalidated
        session_id = request.session.get("session_id", "")
        if session_id.startswith("INVALIDATED_"):
            request.session.clear()
            return False
        
        # Check if admin flag exists and is True
        if not request.session.get("admin", False):
            return False
        
        # Check if session has expired
        expires = request.session.get("expires")
        if expires and expires < 0:  # Past timestamp indicates expired
            request.session.clear()
            return False
        
        # Check if user still exists and is active (additional security)
        user_id = request.session.get("user_id")
        if user_id:
            try:
                async with AsyncSessionLocal() as session:
                    result = await session.execute(
                        select(User).where(User.id == user_id)
                    )
                    user = result.scalar_one_or_none()
                    
                    if not user or not user.is_active:
                        request.session.clear()
                        return False
                        
            except Exception:
                # If there's any error checking the user, clear session for security
                request.session.clear()
                return False
        
        return True 