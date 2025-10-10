#!/usr/bin/env python3
"""
FastOpp Base Assets
A minimal FastAPI application with authentication and protected content
"""
import os
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin.setup import setup_admin
from base_assets.routes.auth import router as auth_router
from base_assets.routes.pages import router as pages_router
try:
    from base_assets.routes.oppman import router as oppman_router
except Exception:
    oppman_router = None  # Optional during partial restores

app = FastAPI(
    title="FastOpp Base Assets",
    description="A minimal FastAPI application with authentication and protected content",
    version="1.0.0"
)

"""Configure authentication/session for SQLAdmin login and user authentication"""
# Load environment variables and secret key
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key_change_in_production")

# Enable sessions (required by sqladmin authentication backend)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# SQLAdmin automatically handles static file serving at /admin/statics/
# No manual mounting required - SQLAdmin does this internally

# Mount SQLAdmin with authentication backend
setup_admin(app, SECRET_KEY)


# Add middleware to inject FontAwesome CDN CSS for reliable icon display
@app.middleware("http")
async def inject_fontawesome_cdn(request, call_next):
    """Inject FontAwesome CDN CSS to fix SQLAdmin boolean icons"""
    response = await call_next(request)
    
    # Only inject CSS for SQLAdmin pages with HTML content
    if (request.url.path.startswith("/admin") and 
        response.headers.get("content-type", "").startswith("text/html") and
        hasattr(response, 'body') and 
        response.body is not None):
        
        try:
            # Inject FontAwesome CDN CSS into the HTML head
            html = response.body.decode("utf-8")
            if "<head>" in html and "font-awesome" not in html.lower():
                cdn_css = '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" integrity="sha512-Avb2QiuDEEvB4bZJYdft2qNjV4BKRQ0w/0f7Kf1L6J6gI5P1eF6E1C5g6e2BV3kpJ4lQRdXf34xe4k1zQ3PJV+Q==" crossorigin="anonymous" referrerpolicy="no-referrer">'
                html = html.replace("<head>", f"<head>{cdn_css}")
                response.body = html.encode("utf-8")
        except Exception:
            # If there's any error with the middleware, just pass through
            pass
    
    return response

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth_router)
app.include_router(pages_router)
if oppman_router:
    app.include_router(oppman_router, prefix="/oppman")

# Add exception handler for authentication


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and redirect to login if authentication fails"""
    if exc.status_code in [401, 403]:
        return RedirectResponse(url="/login", status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "FastOpp Base Assets app is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
