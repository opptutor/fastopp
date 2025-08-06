"""
Authentication routes
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from db import AsyncSessionLocal
from models import User
from auth import create_user_token
from fastapi_users.password import PasswordHelper

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page for webinar registrants access"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "current_page": "login"
    })


@router.post("/login")
async def login_form(request: Request):
    """Handle login form submission"""
    form = await request.form()
    username = form.get("username")
    password = form.get("password")

    if not username or not password:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "title": "Login",
            "current_page": "login",
            "error": "Please provide both email and password"
        })
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == username)
        )
        user = result.scalar_one_or_none()

        if not user:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Invalid email or password"
            })

        password_helper = PasswordHelper()
        if not password_helper.verify_and_update(str(password), user.hashed_password):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Invalid email or password"
            })

        if not user.is_active:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Account is inactive"
            })

        if not (user.is_staff or user.is_superuser):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "title": "Login",
                "current_page": "login",
                "error": "Access denied. Staff or admin privileges required."
            })

        # Create session token
        token = create_user_token(user)
        response = RedirectResponse(url="/webinar-registrants", status_code=302)
        response.set_cookie(key="access_token", value=token, httponly=True, max_age=1800)  # 30 minutes
        return response


@router.get("/logout")
async def logout():
    """Logout and clear authentication cookie"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response 