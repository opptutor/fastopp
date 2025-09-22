"""
API routes for data endpoints
"""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from models import User
from auth.core import get_current_staff_or_admin_from_cookies
from dependencies.services import get_product_service, get_webinar_service
from services.product_service import ProductService
from services.webinar_service import WebinarService

router = APIRouter()


@router.get("/products", response_model=None)
async def get_products():
    """API endpoint to fetch product data for the dashboard"""
    # Simple mock data for now
    data = {
        "products": [
            {"id": 1, "name": "Test Product 1", "price": 10.99, "stock": 100},
            {"id": 2, "name": "Test Product 2", "price": 20.99, "stock": 50},
        ],
        "total_products": 2,
        "total_value": 31.98
    }
    return JSONResponse(data)


@router.get("/registrants", response_model=None)
async def get_registrants(
    current_user: User = Depends(get_current_staff_or_admin_from_cookies)
):
    """Get all webinar registrants with their photos"""
    # Simple mock data for now
    registrants = [
        {"id": 1, "name": "John Doe", "email": "john@example.com", "photo_url": None},
        {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "photo_url": None},
    ]
    return JSONResponse({"registrants": registrants})


@router.get("/webinar-attendees", response_model=None)
async def get_webinar_attendees(
    request: Request
):
    """Get webinar attendees for the marketing demo page"""
    from fastapi.templating import Jinja2Templates
    
    # Simple mock data for now
    attendees = [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com", "attendance_status": "attended"},
    ]
    
    # Check if this is an HTMX request
    templates = Jinja2Templates(directory="templates")
    
    # Return HTML for HTMX requests, JSON for API requests
    if 'hx-request' in request.headers:
        return templates.TemplateResponse("partials/attendees-grid.html", {
            "request": request,
            "attendees": attendees
        })
    else:
        return JSONResponse(attendees) 