# =========================
# main.py
# =========================
import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import select, func
from sqlalchemy import case
from db import AsyncSessionLocal
from models import User, Product
from auth import create_user_token
from fastapi_users.password import PasswordHelper
from dotenv import load_dotenv
from admin.setup import setup_admin

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


@app.get("/dashboard-demo", response_class=HTMLResponse)
async def dashboard_demo(request: Request):
    return templates.TemplateResponse("dashboard-demo.html", {"request": request, "title": "Product Dashboard Demo"})


@app.get("/api/products")
async def get_products():
    """API endpoint to fetch product data for the dashboard"""
    async with AsyncSessionLocal() as session:
        # Get all products
        result = await session.execute(select(Product))
        products = result.scalars().all()
        
        # Get category statistics
        category_stats = await session.execute(
            select(Product.category, func.count(Product.id).label('count'))
            .group_by(Product.category)
        )
        categories = category_stats.all()
        
        # Get price statistics
        price_stats = await session.execute(
            select(
                func.avg(Product.price).label('avg_price'),
                func.min(Product.price).label('min_price'),
                func.max(Product.price).label('max_price'),
                func.count(Product.id).label('total_products')
            )
        )
        stats = price_stats.first()
        
        # Get stock statistics
        stock_stats = await session.execute(
            select(
                func.count(Product.id).label('total'),
                func.sum(case((Product.in_stock.is_(True), 1), else_=0)).label('in_stock'),
                func.sum(case((Product.in_stock.is_(False), 1), else_=0)).label('out_of_stock')
            )
        )
        stock = stock_stats.first()
        
        # Handle potential None values safely
        stats_data = {
            "avg_price": float(stats.avg_price) if stats and stats.avg_price is not None else 0,
            "min_price": float(stats.min_price) if stats and stats.min_price is not None else 0,
            "max_price": float(stats.max_price) if stats and stats.max_price is not None else 0,
            "total_products": stats.total_products if stats else 0
        }
        
        stock_data = {
            "total": stock.total if stock else 0,
            "in_stock": stock.in_stock if stock else 0,
            "out_of_stock": stock.out_of_stock if stock else 0
        }
        
        return JSONResponse({
            "products": [
                {
                    "id": str(product.id),
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "category": product.category,
                    "in_stock": product.in_stock,
                    "created_at": product.created_at.isoformat()
                }
                for product in products
            ],
            "categories": [
                {"category": cat.category, "count": cat.count}
                for cat in categories if cat.category
            ],
            "stats": stats_data,
            "stock": stock_data
        })


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

# Setup admin interface
setup_admin(app, SECRET_KEY)
