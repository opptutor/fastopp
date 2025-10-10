# SQLAdmin Icons Fix for LeapCell Deployment

## Problem Description

When deploying FastOpp to LeapCell, SQLAdmin interface displays broken icons in boolean columns (`is_active`, `is_superuser`, `is_staff`). Instead of proper checkmark/X icons, you see small colored squares with broken text like "Fo" and "F1".

## Root Cause

The issue occurs because SQLAdmin's static assets (CSS, JavaScript, and icon files) are not being properly served in the LeapCell production environment. SQLAdmin relies on these static files to display icons correctly.

**Important Discovery**: SQLAdmin stores its static files in a directory called `statics` (plural), not `static` (singular). The static files include:
- CSS files: `main.css`, `fontawesome.min.css`, `tabler-icons.min.css`, etc.
- Icon fonts: `tabler-icons.woff2`, `fa-solid-900.woff2`, etc.
- JavaScript files: `main.js`, `bootstrap.min.js`, etc.

**Critical Path Fix**: SQLAdmin expects static files to be served at `/admin/statics/`, not `/sqladmin/static/`. This path mismatch was causing the 404 errors for font files.

## Solution Implemented

### 1. Static File Mounting

Added proper mounting of SQLAdmin static files in `main.py`:

```python
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
```

### 2. Fallback Route Handler

Added a custom route handler as a fallback for SQLAdmin static files:

```python
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
```

### 3. Production Environment Detection

Updated the admin setup to properly detect LeapCell deployments:

```python
# Check if we're in production (HTTPS environment)
is_production = (os.getenv("RAILWAY_ENVIRONMENT") or
                 os.getenv("PRODUCTION") or
                 os.getenv("FORCE_HTTPS") or
                 os.getenv("ENVIRONMENT") == "production" or
                 os.getenv("LEAPCELL_ENVIRONMENT") or
                 "leapcell" in os.getenv("DATABASE_URL", "").lower())
```

## Files Modified

1. **`main.py`** - Added SQLAdmin static file mounting and fallback route
2. **`admin/setup.py`** - Enhanced production environment detection for LeapCell
3. **`base_assets/main.py`** - Added SQLAdmin static file mounting and fallback route
4. **`base_assets/admin/setup.py`** - Enhanced production environment detection for LeapCell

## How It Works

1. **Primary Solution**: The static file mount ensures SQLAdmin's CSS and icon files are served from the correct path
2. **Fallback Solution**: The custom route handler provides an alternative way to serve these files if the mount fails
3. **Production Detection**: Enhanced detection ensures proper configuration for LeapCell deployments

## Testing the Fix

### Local Testing

1. Run the application locally:
   ```bash
   uv run python main.py
   ```

2. Check the console output for SQLAdmin static file mounting messages:
   ```
   ✅ SQLAdmin static files mounted at: /path/to/sqladmin/static
   ```

3. Visit the admin interface and verify icons display correctly

### LeapCell Deployment

1. Deploy your application to LeapCell with the updated code
2. Check the application logs for SQLAdmin static file mounting messages
3. Visit your admin interface at `https://your-app.leapcell.com/admin/`
4. Verify that boolean columns now show proper checkmark/X icons instead of broken squares

## Troubleshooting

### Icons Still Not Displaying

1. **Check Application Logs**: Look for SQLAdmin static file mounting messages
2. **Verify File Paths**: Ensure SQLAdmin static files exist in the expected location
3. **Browser Developer Tools**: Check the Network tab for failed requests to static files
4. **Manual Testing**: Try accessing a static file directly (e.g., `/sqladmin/static/css/admin.css`)

### Common Issues

- **Import Errors**: Ensure SQLAdmin is properly installed
- **Path Issues**: Check that the SQLAdmin static directory exists
- **Permission Issues**: Verify file system permissions in production
- **Caching**: Clear browser cache to see updated static files

## Additional Notes

- This fix is backward compatible and won't affect local development
- The solution works for all deployment platforms (LeapCell, Railway, Fly.io, etc.)
- No changes to your database or existing functionality
- The fix is automatically applied when you deploy the updated code

## Support

If you continue to experience issues:

1. Check the application logs for error messages
2. Verify that SQLAdmin is properly installed in your environment
3. Test the static file endpoints manually
4. Consider using browser developer tools to debug network requests
