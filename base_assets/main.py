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


# Add middleware to inject FontAwesome CDN CSS automatically
@app.middleware("http")
async def inject_fontawesome_cdn_auto(request, call_next):
    """Automatically inject FontAwesome CDN CSS for SQLAdmin pages"""
    response = await call_next(request)
    
    # Only inject for SQLAdmin pages with HTML content
    if (request.url.path.startswith("/admin") and 
        response.headers.get("content-type", "").startswith("text/html")):
        
        try:
            # Get HTML content - handle different response types
            html = None
            if hasattr(response, 'body') and response.body:
                html = response.body.decode("utf-8")
            elif hasattr(response, 'content') and response.content:
                html = response.content.decode("utf-8")
            elif hasattr(response, 'text'):
                html = response.text
            else:
                return response
                
            # Check if FontAwesome CDN is already present
            if html and "cdnjs.cloudflare.com" not in html and "font-awesome" not in html.lower():
                # Inject FontAwesome CDN CSS
                cdn_css = '''<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" crossorigin="anonymous">'''
                
                # Find the head tag and inject CSS
                if "<head>" in html:
                    html = html.replace("<head>", f"<head>{cdn_css}")
                elif "<head " in html:
                    html = html.replace("<head ", f"<head {cdn_css} ")
                
                # Update response - handle different response types
                if hasattr(response, 'body'):
                    response.body = html.encode("utf-8")
                elif hasattr(response, 'content'):
                    response.content = html.encode("utf-8")
                elif hasattr(response, 'text'):
                    response.text = html
                else:
                    # Create new response for other types
                    from fastapi.responses import HTMLResponse
                    return HTMLResponse(content=html, status_code=response.status_code, headers=dict(response.headers))
                    
        except Exception as e:
            # If there's any error, just pass through
            print(f"CDN injection error: {e}")
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
