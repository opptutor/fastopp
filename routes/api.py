"""
API routes for data endpoints
"""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from models import User
from auth import get_current_staff_or_admin_from_cookies

router = APIRouter()


@router.get("/products")
async def get_products():
    """API endpoint to fetch product data for the dashboard"""
    from services.product_service import ProductService
    
    data = await ProductService.get_products_with_stats()
    return JSONResponse(data)


@router.get("/registrants")
async def get_registrants(current_user: User = Depends(get_current_staff_or_admin_from_cookies)):
    """Get all webinar registrants with their photos"""
    from services.webinar_service import WebinarService
    
    registrants = await WebinarService.get_all_registrants()
    return JSONResponse({"registrants": registrants})


@router.get("/webinar-attendees")
async def get_webinar_attendees():
    """Get webinar attendees for the marketing demo page"""
    from services.webinar_service import WebinarService
    
    attendees = await WebinarService.get_webinar_attendees()
    return JSONResponse({"attendees": attendees}) 