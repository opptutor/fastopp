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

# Mount SQLAdmin static files for proper icon and CSS serving
# This ensures SQLAdmin assets are accessible in production deployments
try:
    import sqladmin
    import os
    sqladmin_static_path = os.path.join(os.path.dirname(sqladmin.__file__), "statics")
    if os.path.exists(sqladmin_static_path):
        # Mount at the path SQLAdmin expects: /admin/statics/
        app.mount("/admin/statics", StaticFiles(directory=sqladmin_static_path), name="sqladmin_static")
        print(f"✅ SQLAdmin static files mounted at: {sqladmin_static_path}")
        print(f"✅ Mounted at path: /admin/statics/")
    else:
        print(f"⚠️  SQLAdmin static path not found: {sqladmin_static_path}")
except ImportError:
    print("⚠️  SQLAdmin not available for static file mounting")
except Exception as e:
    print(f"⚠️  Error mounting SQLAdmin static files: {e}")

# Mount SQLAdmin with authentication backend
setup_admin(app, SECRET_KEY)


# Add custom route for SQLAdmin static files as fallback
@app.get("/admin/statics/{file_path:path}")
async def sqladmin_static_fallback(file_path: str):
    """Fallback handler for SQLAdmin static files"""
    try:
        import sqladmin
        import os
        sqladmin_static_path = os.path.join(os.path.dirname(sqladmin.__file__), "statics")
        full_path = os.path.join(sqladmin_static_path, file_path)

        if os.path.exists(full_path) and os.path.isfile(full_path):
            return FileResponse(full_path)
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception:
        raise HTTPException(status_code=404, detail="SQLAdmin static file not available")

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
