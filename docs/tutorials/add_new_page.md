# Add New Page

This guide covers adding new pages, testing, debugging, and best practices for the FastOpp application.

## Adding New Pages

### Overview

The Migration Guide page is a static documentation page that doesn't require any database models. It's purely a frontend page that displays information about how to use the existing migration system.

### Key Steps

1. Create a new template for the page
2. Add a route for the page
3. Update the header navigation
4. Add a card to the homepage

### Example: Adding Migration Guide Page

#### 1. Create Template

Create `templates/migration-guide.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Migration Guide - FastOpp</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@4.7.2/dist/full.min.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <div x-data="{ mobileMenuOpen: false }">
        <!-- Navigation content -->
    </div>

    <!-- Hero Section -->
    <div class="bg-gradient-to-r from-green-600 to-green-800 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-5xl font-bold mb-6">Migration Guide</h1>
            <p class="text-xl mb-8">Learn how to manage database migrations in your FastAPI application</p>
            <div class="flex justify-center space-x-4">
                <a href="#quick-start" class="bg-white text-green-800 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                    Quick Start
                </a>
                <a href="#commands" class="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-green-800 transition-colors">
                    Commands
                </a>
            </div>
        </div>
    </div>

    <!-- Content Sections -->
    <div class="container mx-auto px-4 py-16">
        <!-- Quick Start Section -->
        <section id="quick-start" class="mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Quick Start Guide</h2>
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Step cards -->
            </div>
        </section>

        <!-- Commands Section -->
        <section id="commands" class="mb-16">
            <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Migration Commands</h2>
            <!-- Command tables -->
        </section>
    </div>
</body>
</html>
```

#### 2. Add Route

Update `routes/pages.py`:

```python
@router.get("/migration-guide")
async def migration_guide(request: Request):
    """Migration Guide page"""
    return templates.TemplateResponse("migration-guide.html", {"request": request})
```

#### 3. Update Navigation

Update `templates/partials/header.html`:

```html
<nav class="hidden md:flex space-x-8">
    <a href="/" class="text-gray-300 hover:text-white transition-colors">Home</a>
    <a href="/migration-guide" class="text-gray-300 hover:text-white transition-colors">Migration Guide</a>
    <a href="/webinar-demo" class="text-gray-300 hover:text-white transition-colors">Webinar Demo</a>
    <!-- Other navigation items -->
</nav>
```

#### 4. Add Homepage Card

Update `templates/index.html`:

```html
<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
    <!-- Existing cards -->
    
    <!-- Migration Guide Card -->
    <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
        <div class="flex items-center mb-4">
            <svg class="w-8 h-8 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
            <h3 class="text-xl font-semibold">Migration Guide</h3>
        </div>
        <p class="text-green-100 mb-4">Learn how to manage database migrations with Alembic in your FastAPI application.</p>
        <a href="/migration-guide" class="inline-block bg-white text-green-600 px-4 py-2 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
            Get Started
        </a>
    </div>
</div>
```

## Development Workflow

### 1. Environment Setup

Ensure your development environment is properly configured:

```bash
# Check environment
python oppman.py env

# Verify database connection
python oppman.py migrate current

# Check dependencies
uv sync
```

### 2. Development Server

Start the development server:

```bash
# Start development server
python oppman.py runserver

# Or use uvicorn directly
uv run uvicorn main:app --reload
```

### 3. Database Management

```bash
# Create new migration
python oppman.py migrate create "Description of changes"

# Apply migrations
python oppman.py migrate upgrade

# Check migration status
python oppman.py migrate current
```

### 4. Testing Changes

```bash
# Test database operations
python oppman.py migrate check

# Test authentication
python -m scripts.test_auth

# Test user management
python -m scripts.check_users
```

## Development Patterns

### 1. Model-View-Service (MVS) Architecture

Follow the established MVS pattern:

- **Models** (`models.py`): Data structures and database models
- **Views** (`routes/`): HTTP endpoints and request handling
- **Services** (`services/`): Business logic and data operations

### 2. Route Organization

Organize routes by functionality:

```python
# routes/pages.py - Page rendering routes
@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# routes/api.py - JSON API endpoints
@router.get("/api/data")
async def get_data():
    return {"data": "example"}

# routes/auth.py - Authentication routes
@router.post("/login")
async def login():
    # Login logic
    pass
```

### 3. Service Layer

Implement business logic in services:

```python
# services/product_service.py
class ProductService:
    @staticmethod
    async def get_products():
        # Database query logic
        pass
    
    @staticmethod
    async def create_product(product_data):
        # Product creation logic
        pass
```

### 4. Template Structure

Use consistent template organization:

```
templates/
├── index.html              # Homepage
├── partials/               # Reusable components
│   ├── header.html         # Navigation header
│   ├── footer.html         # Page footer
│   └── sidebar.html        # Sidebar navigation
├── pages/                  # Page-specific templates
│   ├── dashboard.html      # Dashboard page
│   └── profile.html        # User profile page
└── components/             # Reusable UI components
    ├── forms.html          # Form components
    └── tables.html         # Table components
```

## Testing and Debugging

### 1. Testing New Features

#### Manual Testing
1. Start development server
2. Navigate to new page/feature
3. Test all functionality
4. Check error handling
5. Verify responsive design

#### Automated Testing
```bash
# Run tests
uv run python -m pytest

# Run specific test file
uv run python -m pytest tests/test_pages.py

# Run with coverage
uv run python -m pytest --cov=.
```

### 2. Debugging Techniques

#### Logging
```python
import logging

logger = logging.getLogger(__name__)

@router.get("/debug")
async def debug_endpoint():
    logger.debug("Debug endpoint accessed")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    return {"status": "debug"}
```

#### Debug Mode
```python
# Enable debug mode
import debugpy
debugpy.listen(("0.0.0.0", 5678))

# Connect with VS Code or other debugger
```

#### HTMX Debugging
```html
<!-- Enable HTMX debugging -->
<script>
    htmx.logAll();
</script>

<!-- Debug HTMX requests -->
<div hx-get="/api/data" 
     hx-trigger="click"
     hx-debug="true">
    Click to load data
</div>
```

### 3. Common Issues and Solutions

#### HTMX Loading Issues
If automatic loading doesn't work:

```javascript
// Add fallback for HTMX load triggers
setTimeout(() => {
    const container = document.getElementById('container');
    if (container && container.innerHTML.includes('Loading...')) {
        htmx.trigger(container, 'load');
    }
}, 500);
```

#### Database Connection Issues
```bash
# Check database status
python oppman.py env

# Verify migrations
python oppman.py migrate current

# Test database connection
python -c "from db import AsyncSessionLocal; print('DB connection OK')"
```

#### Template Rendering Issues
```python
# Check template path
print(templates.directory)

# Verify template exists
import os
template_path = "templates/index.html"
print(f"Template exists: {os.path.exists(template_path)}")
```

## Code Standards

### 1. Python Style

Follow PEP 8 guidelines:

```python
# Good
def get_user_by_id(user_id: str) -> Optional[User]:
    """Get user by ID from database."""
    return db.query(User).filter(User.id == user_id).first()

# Avoid
def getUserById(userId):
    return db.query(User).filter(User.id==userId).first()
```

### 2. Type Hints

Use type hints consistently:

```python
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel

async def create_user(
    user_data: Dict[str, Any],
    db: AsyncSession
) -> User:
    """Create a new user."""
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

### 3. Error Handling

Implement proper error handling:

```python
from fastapi import HTTPException

@router.get("/users/{user_id}")
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### 4. Documentation

Document your code:

```python
async def process_webinar_registration(
    registration_data: WebinarRegistration,
    db: AsyncSession
) -> WebinarRegistrant:
    """
    Process a new webinar registration.
    
    Args:
        registration_data: Registration information from form
        db: Database session
        
    Returns:
        Created webinar registrant record
        
    Raises:
        HTTPException: If registration validation fails
    """
    # Implementation
    pass
```

## Performance Optimization

### 1. Database Queries

Optimize database operations:

```python
# Use select() for better performance
from sqlalchemy import select

# Good
stmt = select(User).where(User.is_active == True)
users = await db.execute(stmt)

# Avoid
users = await db.query(User).filter(User.is_active == True).all()
```

### 2. Caching

Implement caching for expensive operations:

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_configuration():
    """Cache configuration data."""
    return load_config_from_file()

# Or use Redis for distributed caching
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_cached_data(key: str):
    data = redis_client.get(key)
    if not data:
        data = await fetch_data_from_database()
        redis_client.setex(key, 3600, data)  # Cache for 1 hour
    return data
```

### 3. Async Operations

Use async/await properly:

```python
# Good - concurrent operations
async def get_user_data(user_id: str):
    async with httpx.AsyncClient() as client:
        user_response, profile_response = await asyncio.gather(
            client.get(f"/api/users/{user_id}"),
            client.get(f"/api/users/{user_id}/profile")
        )
        return user_response.json(), profile_response.json()

# Avoid - sequential operations
async def get_user_data(user_id: str):
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"/api/users/{user_id}")
        profile_response = await client.get(f"/api/users/{user_id}/profile")
        return user_response.json(), profile_response.json()
```

## Deployment Preparation

### 1. Environment Configuration

Prepare for production:

```bash
# Create production .env
cp .env .env.production

# Update production values
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/db
ENVIRONMENT=production
DEBUG=false
```

### 2. Database Migrations

Ensure migrations are ready:

```bash
# Check migration status
python oppman.py migrate check

# Create production migration if needed
python oppman.py migrate create "Production preparation"

# Test migrations
python oppman.py migrate upgrade
```

### 3. Static Files

Prepare static assets:

```bash
# Collect static files
python -m scripts.collect_static

# Optimize images
python -m scripts.optimize_images

# Generate favicon
python -m scripts.generate_favicon
```

## Next Steps

After setting up development workflow:

1. **Create New Pages**: Add new features and pages to the application
2. **Implement Testing**: Add automated tests for new functionality
3. **Optimize Performance**: Monitor and improve application performance
4. **Prepare for Production**: Ensure code is production-ready

For more information, see:
- [POSTGRESQL_SETUP.md](deployment/POSTGRESQL_SETUP.md) - PostgreSQL setup and database configuration
- [DATABASE.md](DATABASE.md) - Database management and migrations
- [FEATURES.md](FEATURES.md) - Application features and usage
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture overview
