# SQLAdmin HTTPS Mixed Content Fix

## Problem Description

When deploying FastAPI applications with SQLAdmin to production environments (especially Railway), you may encounter "Mixed Content" errors where the admin interface tries to load CSS and JavaScript files over HTTP instead of HTTPS. This happens because:

1. **Production serves over HTTPS** (Railway, Fly.io, etc.)
2. **SQLAdmin generates static asset URLs** based on the request scheme
3. **Proxy headers aren't properly handled**, causing the app to think it's running on HTTP
4. **Browser blocks mixed content** (HTTPS page loading HTTP resources)

## Error Example

```
Mixed Content: The page at 'https://your-app.railway.app/admin/' was loaded over HTTPS, 
but requested an insecure stylesheet 'http://your-app.railway.app/admin/statics/css/tabler.min.css'. 
This request has been blocked; the content must be served over HTTPS.
```

## Solution

### 1. Update Admin Setup (`admin/setup.py`)

```python
import os
from sqladmin import Admin
from fastapi import FastAPI
from db import async_engine
from auth.admin import AdminAuth
from .views import UserAdmin, ProductAdmin, WebinarRegistrantsAdmin, AuditLogAdmin


def setup_admin(app: FastAPI, secret_key: str):
    """Setup and configure the admin interface"""
    # Check if we're in production (HTTPS environment)
    is_production = os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("PRODUCTION") or os.getenv("FORCE_HTTPS")
    
    # Configure admin with HTTPS support for production
    admin_config = {
        "app": app,
        "engine": async_engine,
        "authentication_backend": AdminAuth(secret_key=secret_key),
    }
    
    # Add HTTPS configuration for production
    if is_production:
        admin_config.update({
            "base_url": "/admin",
            "title": "FastOpp Admin",
            "logo_url": None,  # Disable logo to avoid mixed content issues
        })
    
    admin = Admin(**admin_config)
    
    # Register admin views
    admin.add_view(UserAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(WebinarRegistrantsAdmin)
    admin.add_view(AuditLogAdmin)
    return admin
```

### 2. Add Proxy Headers Middleware (`main.py`)

```python
from starlette.middleware.base import BaseHTTPMiddleware

class ProxyHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to handle proxy headers for production deployments"""
    
    async def dispatch(self, request: Request, call_next):
        # Check if we're behind a proxy (Railway, Fly, etc.)
        if request.headers.get("x-forwarded-proto") == "https":
            request.scope["scheme"] = "https"
        
        # Don't modify scope["type"] - it should remain "http" for HTTP requests
        
        response = await call_next(request)
        return response

# Add to your FastAPI app
app.add_middleware(ProxyHeadersMiddleware)
```

### 3. Add Production Middleware (`main.py`)

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Add middleware for production deployment
app.add_middleware(ProxyHeadersMiddleware)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
```

## Environment Variables

Set one of these environment variables in production to enable HTTPS mode:

```bash
# Railway
RAILWAY_ENVIRONMENT=production

# Generic
PRODUCTION=true

# Force HTTPS
FORCE_HTTPS=true
```

## Why This Fix Works

1. **Proxy Headers**: Detects when the app is behind an HTTPS proxy
2. **Scheme Override**: Forces the request scheme to HTTPS
3. **SQLAdmin Configuration**: Ensures static assets are served over HTTPS
4. **Production Detection**: Automatically enables HTTPS mode in production

## Platform Compatibility

- ✅ **Railway** - Fixes the mixed content issue
- ✅ **Fly.io** - Maintains existing functionality
- ✅ **Heroku** - Prevents future issues
- ✅ **DigitalOcean App Platform** - Prevents future issues
- ✅ **Local Development** - No impact

## Testing

After deploying the fix:

1. Access your admin interface at `/admin`
2. Check browser console for mixed content errors
3. Verify all CSS/JS files load over HTTPS
4. Admin interface should render properly with styling

## Troubleshooting

### Common Error: `AssertionError` with scope type

If you see errors like:
```
assert scope["type"] in ("http", "websocket", "lifespan")
AssertionError
```

**Problem**: The middleware is incorrectly setting `scope["type"] = "https"`

**Solution**: Only modify `scope["scheme"]`, never `scope["type"]`:

```python
# ✅ CORRECT
if request.headers.get("x-forwarded-proto") == "https":
    request.scope["scheme"] = "https"

# ❌ WRONG - Don't do this!
# request.scope["type"] = "https"
```

### Key Differences

- **`scope["scheme"]`** = protocol (http/https) - used by SQLAdmin for URL generation
- **`scope["type"]`** = request type (http/websocket/lifespan) - must be one of these three values

This fix ensures SQLAdmin works correctly across all production deployment scenarios while maintaining backward compatibility.
