# =========================
# main.py
# =========================
import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic
from starlette.middleware.sessions import SessionMiddleware
from sqlmodel import select, func
from sqlalchemy import case
from db import AsyncSessionLocal
from models import User, Product, WebinarRegistrants
from auth import create_user_token, get_current_staff_or_admin_from_cookies
from fastapi_users.password import PasswordHelper
from dotenv import load_dotenv
from admin.setup import setup_admin

# Load environment variables
load_dotenv()

# Get secret key from environment
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")

# Create upload directories
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
PHOTOS_DIR = UPLOAD_DIR / "photos"
PHOTOS_DIR.mkdir(exist_ok=True)

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


@app.get("/webinar-registrants", response_class=HTMLResponse)
async def webinar_registrants(request: Request, current_user: User = Depends(get_current_staff_or_admin_from_cookies)):
    return templates.TemplateResponse("webinar-registrants.html", {
        "request": request, 
        "title": "Webinar Registrants",
        "current_page": "webinar-registrants"
    })


@app.get("/api/products")
async def get_products():
    """API endpoint to fetch product data for the dashboard"""
    async with AsyncSessionLocal() as session:
        # Get all products
        result = await session.execute(select(Product))
        products = result.scalars().all()

        # Get category statistics
        category_stats = await session.execute(
            select(Product.category, func.count(Product.id).label('count'))  # type: ignore
            .group_by(Product.category)
        )
        categories = category_stats.all()

        # Get price statistics
        price_stats = await session.execute(
            select(
                func.avg(Product.price).label('avg_price'),
                func.min(Product.price).label('min_price'),
                func.max(Product.price).label('max_price'),
                func.count(Product.id).label('total_products')  # type: ignore
            )
        )
        stats = price_stats.first()

        # Get stock statistics
        stock_stats = await session.execute(
            select(
                func.count(Product.id).label('total'),  # type: ignore
                func.sum(case(
                    (Product.in_stock.is_(True), 1),  # type: ignore
                    else_=0)).label('in_stock'),
                func.sum(case(
                    (Product.in_stock.is_(False), 1),  # type: ignore
                    else_=0)).label('out_of_stock')  # type: ignore
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


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page for webinar registrants access"""
    return templates.TemplateResponse("login.html", {
        "request": request,
        "title": "Login",
        "current_page": "login"
    })


@app.post("/login")
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


@app.get("/logout")
async def logout():
    """Logout and clear authentication cookie"""
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="access_token")
    return response


# Setup admin interface
setup_admin(app, SECRET_KEY)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and redirect to login if authentication fails"""
    if exc.status_code in [401, 403]:
        return RedirectResponse(url="/login", status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.post("/upload-photo/{registrant_id}")
async def upload_photo(
    registrant_id: str,
    photo: UploadFile = File(...),
    description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_staff_or_admin_from_cookies)
):
    """Upload a photo for a webinar registrant"""
    
    # Validate file type
    if not photo.content_type or not photo.content_type.startswith('image/'):
        return HTMLResponse(
            '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            'Error: File must be an image</div>',
            status_code=400
        )
    
    # Validate file size (max 5MB)
    if photo.size and photo.size > 5 * 1024 * 1024:
        return HTMLResponse(
            '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            'Error: File size must be less than 5MB</div>',
            status_code=400
        )
    
    # Generate unique filename
    file_extension = Path(photo.filename).suffix if photo.filename else '.jpg'
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = PHOTOS_DIR / unique_filename
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            content = await photo.read()
            buffer.write(content)
    except Exception as e:
        return HTMLResponse(
            '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
            f'Error: Failed to save file: {str(e)}</div>',
            status_code=500
        )
    
    # Update database
    photo_url = f"/static/uploads/photos/{unique_filename}"
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(WebinarRegistrants).where(WebinarRegistrants.id == registrant_id)
        )
        registrant = result.scalar_one_or_none()
        
        if not registrant:
            # Clean up file if registrant not found
            try:
                file_path.unlink()
            except Exception:
                pass
            return HTMLResponse(
                '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
                'Error: Registrant not found</div>',
                status_code=404
            )
        
        registrant.photo_url = photo_url
        await session.commit()
    
    return HTMLResponse(
        '<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">'
        'Photo uploaded successfully!</div>'
    )


@app.get("/registrants")
async def get_registrants(current_user: User = Depends(get_current_staff_or_admin_from_cookies)):
    """Get all webinar registrants with their photos"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(WebinarRegistrants))
        registrants = result.scalars().all()
        
        return JSONResponse({
            "registrants": [
                {
                    "id": str(registrant.id),
                    "name": registrant.name,
                    "email": registrant.email,
                    "company": registrant.company,
                    "webinar_title": registrant.webinar_title,
                    "webinar_date": registrant.webinar_date.isoformat(),
                    "status": registrant.status,
                    "photo_url": registrant.photo_url,
                    "registration_date": registrant.registration_date.isoformat()
                }
                for registrant in registrants
            ]
        })


@app.delete("/delete-photo/{registrant_id}")
async def delete_photo(registrant_id: str, current_user: User = Depends(get_current_staff_or_admin_from_cookies)):
    """Delete a photo for a webinar registrant"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(WebinarRegistrants).where(WebinarRegistrants.id == registrant_id)
        )
        registrant = result.scalar_one_or_none()
        
        if not registrant:
            return HTMLResponse(
                '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
                'Error: Registrant not found</div>',
                status_code=404
            )
        
        if not registrant.photo_url:
            return HTMLResponse(
                '<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">'
                'Error: No photo found for this registrant</div>',
                status_code=404
            )
        
        # Delete file from filesystem
        photo_path = Path("static") / registrant.photo_url.lstrip("/static/")
        try:
            if photo_path.exists():
                photo_path.unlink()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to delete file {photo_path}: {e}")
        
        # Update database
        registrant.photo_url = None
        await session.commit()
    
    return HTMLResponse(
        '<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded">'
        'Photo deleted successfully!</div>'
    )
