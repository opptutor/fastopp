# =========================
# admin_auth.py - SQLAdmin authentication
# =========================
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Handle admin login"""
        form = await request.form()
        username, password = form["username"], form["password"]
        
        # For now, use a simple check - in production, verify against database
        if username == "admin@example.com" and password == "admin123":
            request.session.update({"admin": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        """Handle admin logout"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Check if user is authenticated"""
        return request.session.get("admin", False) 