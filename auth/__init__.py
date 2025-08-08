# =========================
# auth/__init__.py
# =========================

from .core import (
    create_access_token,
    verify_token,
    get_current_user,
    get_current_superuser,
    get_current_staff_or_admin,
    create_user_token,
    get_current_user_from_cookies,
    get_current_staff_or_admin_from_cookies,
)
from .users import fastapi_users, auth_backend, get_user_manager
from .admin import AdminAuth

__all__ = [
    # Core authentication
    "create_access_token",
    "verify_token", 
    "get_current_user",
    "get_current_superuser",
    "get_current_staff_or_admin",
    "create_user_token",
    "get_current_user_from_cookies",
    "get_current_staff_or_admin_from_cookies",
    # FastAPI Users
    "fastapi_users",
    "auth_backend",
    "get_user_manager",
    # Admin authentication
    "AdminAuth",
] 