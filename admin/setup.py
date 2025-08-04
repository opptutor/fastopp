# =========================
# admin/setup.py
# =========================
from sqladmin import Admin
from fastapi import FastAPI
from db import async_engine
from admin_auth import AdminAuth
from .views import UserAdmin, ProductAdmin


def setup_admin(app: FastAPI, secret_key: str):
    """Setup and configure the admin interface"""
    admin = Admin(app, async_engine, authentication_backend=AdminAuth(secret_key=secret_key))
    
    # Register admin views
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    
    return admin 