# =========================
# admin/views.py
# =========================
from sqladmin import ModelView
from models import User, Product


class UserAdmin(ModelView, model=User):
    column_list = ["email", "is_active", "is_superuser"]


class ProductAdmin(ModelView, model=Product):
    column_list = ["name", "price", "category", "in_stock", "created_at"]
    column_searchable_list = ["name", "description", "category"] 