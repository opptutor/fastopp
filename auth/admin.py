# =========================
# auth/admin.py - SQLAdmin authentication
# =========================
from typing import Optional
from datetime import datetime, timezone
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from sqlalchemy import select
from dependencies.database import get_db_session
from models import User
from fastapi_users.password import PasswordHelper


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Handle admin login with database verification"""
        form = await request.form()
        username = form.get("username", "")
        password = form.get("password", "")
        
        print(f"🔐 Login attempt for user: {username}")
        
        # Ensure password is a string
        if isinstance(password, str):
            password_str = password
        else:
            # Handle case where password might be UploadFile or other type
            password_str = str(password)
        
        # Verify user against database
        session_factory = request.app.state.session_factory
        async with session_factory() as session:
            result = await session.execute(
                select(User).where(User.email == username)  # type: ignore
            )
            user: Optional[User] = result.scalar_one_or_none()  # type: ignore
            
            if not user:
                print(f"❌ User not found: {username}")
                return False
            
            print(f"✅ User found: {username}, active: {user.is_active}, superuser: {user.is_superuser}, staff: {user.is_staff}")
            
            # Verify password using FastAPI Users password helper
            password_helper = PasswordHelper()
            is_valid = password_helper.verify_and_update(password_str, user.hashed_password)  # type: ignore
            
            # verify_and_update returns (bool, str) - we need the first element
            if isinstance(is_valid, tuple):
                is_valid = is_valid[0]
            
            if not is_valid:
                print(f"❌ Password verification failed for user: {username}")
                return False
            
            print(f"✅ Password verified for user: {username}")
            
            # Check if user is active and has admin access (superuser OR staff)
            if not user.is_active or not (user.is_superuser or user.is_staff):  # type: ignore
                print(f"❌ User access denied: {username} - active: {user.is_active}, superuser: {user.is_superuser}, staff: {user.is_staff}")
                return False
            
            # Store user info in session with group and permissions
            import uuid
            session_id = str(uuid.uuid4())
            session_data = {
                "admin": True,
                "user_id": str(user.id),  # type: ignore
                "user_email": user.email,  # type: ignore
                "is_superuser": user.is_superuser,  # type: ignore
                "is_staff": user.is_staff,  # type: ignore
                "group": user.group,  # type: ignore
                "can_manage_webinars": user.is_superuser or user.group in ["marketing", "sales"],  # type: ignore
                "login_time": datetime.now(timezone.utc).isoformat(),
                "session_id": session_id,  # Unique session identifier
                "logged_out": False  # Track logout status
            }
            
            print(f"📝 Setting session data: {session_data}")
            request.session.update(session_data)
            print(f"✅ Session created successfully for user: {username}")
            return True

    async def logout(self, request: Request) -> bool:
        """Handle admin logout with comprehensive session cleanup"""
        try:
            # Clear all session data
            request.session.clear()
            
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
        print(f"🔍 Authenticate called - Session keys: {list(request.session.keys())}")
        
        # Check if user has been logged out
        if request.session.get("logged_out", False):
            print("❌ User has been logged out")
            request.session.clear()
            return False
        
        # Check if session ID has been invalidated
        session_id = request.session.get("session_id", "")
        if session_id.startswith("INVALIDATED_"):
            print("❌ Session ID has been invalidated")
            request.session.clear()
            return False
        
        # Check if admin flag exists and is True
        admin_flag = request.session.get("admin", False)
        print(f"🔍 Admin flag: {admin_flag}")
        if not admin_flag:
            print("❌ Admin flag is False or missing")
            return False
        
        # Check if session has expired (expires is a timestamp, not duration)
        login_time = request.session.get("login_time")
        print(f"🔍 Login time: {login_time}")
        if login_time:
            try:
                login_dt = datetime.fromisoformat(login_time.replace('Z', '+00:00'))
                current_dt = datetime.now(timezone.utc)
                # Check if more than 1 hour has passed since login
                time_diff = (current_dt - login_dt).total_seconds()
                print(f"🔍 Time since login: {time_diff} seconds")
                if time_diff > 3600:
                    print("❌ Session expired (more than 1 hour)")
                    request.session.clear()
                    return False
            except Exception as e:
                print(f"❌ Error parsing login time: {e}")
                # If there's any error parsing the time, clear session for security
                request.session.clear()
                return False
        
        # Check if user still exists and is active (additional security)
        user_id = request.session.get("user_id")
        print(f"🔍 User ID from session: {user_id}")
        if user_id:
            try:
                # Convert string user_id to UUID for the database query
                import uuid
                user_uuid = uuid.UUID(user_id)
                
                session_factory = request.app.state.session_factory
                async with session_factory() as session:
                    result = await session.execute(
                        select(User).where(User.id == user_uuid)
                    )
                    user = result.scalar_one_or_none()
                    
                    if not user or not user.is_active:
                        print(f"❌ User not found or inactive: {user_id}")
                        request.session.clear()
                        return False
                    else:
                        print(f"✅ User verified: {user.email}, active: {user.is_active}")
                        
            except Exception as e:
                print(f"❌ Error checking user: {e}")
                # If there's any error checking the user, clear session for security
                request.session.clear()
                return False
        
        print("✅ Authentication successful")
        return True 