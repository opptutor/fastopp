# =========================
# main.py
# =========================
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from admin.setup import setup_admin
from routes.chat import router as chat_router
from routes.api import router as api_router
from routes.health import router as health_router
try:
    from routes.auth import router as auth_router
except Exception:
    auth_router = None  # Optional during partial restores
from routes.pages import router as pages_router
try:
    from routes.webinar import router as webinar_router
except Exception:
    webinar_router = None  # Optional during partial restores
try:
    from routes.oppman import router as oppman_router
except Exception:
    oppman_router = None  # Optional during partial restores
try:
    from routes.oppdemo import router as oppdemo_router
except Exception:
    oppdemo_router = None  # Optional during partial restores

# Import dependency injection modules
from dependencies.database import create_database_engine, create_session_factory
from dependencies.config import get_settings

# Load environment variables
load_dotenv()

# Get settings using dependency injection
settings = get_settings()

# Create upload directories
UPLOAD_DIR = Path(settings.upload_dir)
UPLOAD_DIR.mkdir(exist_ok=True)
PHOTOS_DIR = UPLOAD_DIR / "photos"
PHOTOS_DIR.mkdir(exist_ok=True)

# from users import fastapi_users, auth_backend  # type: ignore

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


# Add proxy headers middleware for production deployments
@app.middleware("http")
async def proxy_headers_middleware(request: Request, call_next):
    """Middleware to handle proxy headers for production deployments"""
    # Check if we're behind a proxy (Railway, Fly, etc.)
    if request.headers.get("x-forwarded-proto") == "https":
        request.scope["scheme"] = "https"

    # Don't modify scope["type"] - it should remain "http" for HTTP requests

    response = await call_next(request)
    return response


# Setup dependencies
def setup_dependencies(app: FastAPI):
    """Setup application dependencies"""
    # Create database engine and session factory
    engine = create_database_engine(settings)
    session_factory = create_session_factory(engine)

    # Store in app state for dependency injection
    app.state.db_engine = engine
    app.state.session_factory = session_factory
    app.state.settings = settings

    print(f"✅ Dependencies setup complete - session_factory: {session_factory}")
    print(f"✅ App state after setup: {list(app.state.__dict__.keys())}")


# Setup dependencies immediately
setup_dependencies(app)

# Mount uploads directory based on environment (MUST come before /static mount)
if settings.upload_dir != "static/uploads":
    # In production environments, mount the uploads directory separately
    app.mount("/static/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Mount static files (MUST come after /static/uploads to avoid conflicts)
app.mount("/static", StaticFiles(directory="static"), name="static")

# SQLAdmin automatically handles static file serving at /admin/statics/
# No manual mounting required - SQLAdmin does this internally

templates = Jinja2Templates(directory="templates")
security = HTTPBasic()


# Setup admin interface
setup_admin(app, settings.secret_key)

# Add a custom route to inject FontAwesome CDN CSS into admin pages
@app.get("/admin/")
async def admin_with_cdn():
    """Redirect to admin with CDN CSS injection"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/admin/", status_code=302)

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

# Include routers
app.include_router(health_router)
app.include_router(chat_router, prefix="/api")
app.include_router(api_router, prefix="/api")
if auth_router:
    app.include_router(auth_router)
app.include_router(pages_router)
if webinar_router:
    app.include_router(webinar_router)
if oppman_router:
    app.include_router(oppman_router, prefix="/oppman")
if oppdemo_router:
    app.include_router(oppdemo_router)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions and redirect to login if authentication fails"""
    if exc.status_code in [401, 403]:
        # Preserve the original URL as a redirect parameter
        original_url = str(request.url)
        login_url = f"/login?next={original_url}"
        return RedirectResponse(url=login_url, status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
