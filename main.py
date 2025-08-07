# =========================
# main.py
# =========================
import os
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from admin.setup import setup_admin
from routes.chat import router as chat_router
from routes.api import router as api_router
from routes.auth import router as auth_router
from routes.pages import router as pages_router
from routes.webinar import router as webinar_router

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


# Setup admin interface
setup_admin(app, SECRET_KEY)

# Include routers
app.include_router(chat_router, prefix="/api")
app.include_router(api_router, prefix="/api")
app.include_router(auth_router)
app.include_router(pages_router)
app.include_router(webinar_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and redirect to login if authentication fails"""
    if exc.status_code in [401, 403]:
        return RedirectResponse(url="/login", status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )