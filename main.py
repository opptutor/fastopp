# =========================
# main.py
# =========================
import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.sessions import SessionMiddleware
from sqladmin import Admin, ModelView
from sqlmodel import select
from db import async_engine, AsyncSessionLocal
from models import User, Product
from auth import create_user_token
from admin_auth import AdminAuth
from fastapi_users.password import PasswordHelper
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get secret key from environment
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")

# from users import fastapi_users, auth_backend  # type: ignore

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Welcome to FastOpp"})


@app.get("/design-demo", response_class=HTMLResponse)
async def design_demo(request: Request):
    return templates.TemplateResponse("design-demo.html", {"request": request, "title": "FastOpp Design Demo"})


@app.get("/ai-stats", response_class=HTMLResponse)
async def ai_stats(request: Request):
    """HTMX endpoint to return AI marketing statistics"""
    import time
    time.sleep(1)  # Simulate processing time
    
    stats = [
        {"metric": "Content Generation Speed", "value": "10x Faster", "icon": "⚡"},
        {"metric": "Campaign ROI", "value": "+340%", "icon": "📈"},
        {"metric": "Time Saved", "value": "87%", "icon": "⏰"},
        {"metric": "Engagement Rate", "value": "+280%", "icon": "🎯"}
    ]
    
    return templates.TemplateResponse("partials/ai-stats.html", {
        "request": request, 
        "stats": stats
    })


@app.post("/marketing-demo", response_class=HTMLResponse)
async def marketing_demo(request: Request):
    """HTMX endpoint to handle marketing demo form submission"""
    # In a real app, you'd parse form data properly
    # For demo purposes, we'll simulate form processing
    import time
    time.sleep(1.5)  # Simulate processing time
    
    return templates.TemplateResponse("partials/demo-response.html", {
        "request": request,
        "success": True,
        "message": "Thank you! Our AI team will contact you within 24 hours with a personalized marketing demo."
    })


@app.post("/login")
async def login(credentials: HTTPBasicCredentials = Depends(security)):
    """Login endpoint for admin access"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == credentials.username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        password_helper = PasswordHelper()
        if not password_helper.verify_and_update(credentials.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Basic"},
            )
        
        if not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        
        token = create_user_token(user)
        return {"access_token": token, "token_type": "bearer"}


# Type warnings are expected with FastAPI Users async setup
# app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])  # type: ignore
# app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])  # type: ignore

admin = Admin(app, async_engine, authentication_backend=AdminAuth(secret_key=SECRET_KEY))


class UserAdmin(ModelView, model=User):
    column_list = ["id", "email", "is_active", "is_superuser"]


class ProductAdmin(ModelView, model=Product):
    column_list = ["id", "name", "price", "category", "in_stock", "created_at"]
    column_searchable_list = ["name", "description", "category"]


admin.add_view(UserAdmin)
admin.add_view(ProductAdmin)
