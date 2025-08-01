# =========================
# main.py
# =========================
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqladmin import Admin, ModelView
from db import async_engine
from models import User
from users import fastapi_users, auth_backend  # type: ignore

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Welcome to FastAPI Admin Demo"})

# Type warnings are expected with FastAPI Users async setup
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])  # type: ignore
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])  # type: ignore

admin = Admin(app, async_engine)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_active, User.is_superuser]


admin.add_view(UserAdmin)
