# FastAPI MVS Architecture

This document outlines the Model-View-Service (MVS) architecture implemented in this FastAPI application.

## Architecture Overview

The application has been refactored from a monolithic `main.py` file into a well-organized structure that separates concerns and improves maintainability.

### Directory Structure

```
fastapi_d/
├── main.py                # New refactored entry point (MVS Architecture)
├── main_old.py            # Original monolithic file (552 lines) - kept for reference
├── routes/                # Route handlers (View layer)
│   ├── __init__.py
│   ├── pages.py          # Page rendering routes
│   ├── auth.py           # Authentication routes
│   ├── api.py            # API data endpoints
│   └── webinar.py        # Webinar management routes
├── services/             # Business logic (Service layer)
│   ├── __init__.py
│   ├── product_service.py
│   └── webinar_service.py
├── models.py             # Data models (Model layer)
├── db.py                 # Database configuration
├── auth.py               # Authentication utilities
└── admin/                # Admin interface
```

## Components

| Functional Concept| Component | Django Equivalent |
| -- | -- | -- |
| Production Web Server | FastAPI + uvicorn (for loads < 1,000 concurrent connections) | NGINX + Gunicorn |
| Development Web Server | uvicorn  | `manage.py runserver` in development. Django Framework |
| Development SQL Database | SQLite | SQLite |
| Production SQL Database | PostgreSQL with pgvector | PostgreSQL + pgvector, asyncpg |
| User Management | [FastAPI Users](https://github.com/fastapi-users/fastapi-users) | Django Admin |
| Database Management | [SQLAdmin](https://aminalaee.github.io/sqladmin/) + Template | Django Admin |
| Authentication | Custom JWT + Session Auth (with database user verification and FastAPI Users password hashing) | Django Admin Auth |

## Project Structure

```text
├── main.py                 # FastAPI application with MVS architecture
├── routes/                 # Route handlers (View layer)
│   ├── pages.py           # HTML page rendering routes
│   ├── auth.py            # Authentication routes
│   ├── api.py             # JSON API endpoints
│   ├── chat.py            # Chat functionality routes
│   └── webinar.py         # Webinar management routes
├── services/              # Business logic (Service layer)
│   ├── product_service.py # Product-related operations
│   ├── webinar_service.py # Webinar registrant operations
│   └── chat_service.py    # Chat functionality operations
├── auth/                  # Authentication module
│   ├── __init__.py       # Module exports and public API
│   ├── core.py           # Core JWT authentication logic
│   ├── users.py          # FastAPI Users integration
│   └── admin.py          # SQLAdmin authentication
├── admin/                 # Admin interface configuration
│   ├── views.py           # Admin view definitions
│   └── setup.py           # Admin interface setup
├── templates/             # Jinja2 templates
│   ├── index.html         # Homepage template
│   ├── login.html         # Login page template
│   ├── design-demo.html   # Static files demo template
│   ├── dashboard-demo.html # Dashboard demo template
│   ├── ai-demo.html       # AI demo template
│   ├── webinar-demo.html  # Webinar demo template
│   ├── webinar-registrants.html # Webinar registrants template
│   └── partials/          # Template partials
│       ├── header.html    # Header partial
│       ├── ai-stats.html  # AI statistics partial
│       └── demo-response.html # Demo response partial
├── static/                # Static assets (images, CSS, JS)
│   ├── images/            # Image files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   ├── favicon.ico        # Site favicon
│   ├── uploads/           # File uploads directory
│   │   ├── photos/        # User uploaded photos
│   │   └── sample_photos/ # Sample photo files
│   └── README.md          # Static files documentation
├── db.py                  # Database configuration (uses environment variables)
├── models.py              # SQLModel models (Model layer)

├── oppman.py              # Management tool for database operations
├── alembic/               # Database migrations
│   ├── env.py             # Alembic environment configuration
│   ├── script.py.mako     # Migration template
│   ├── README             # Migration documentation
│   └── versions/          # Migration files
│       ├── 8e825dae1884_initial_migration.py
│       ├── 6ec04a33369d_add_is_staff_field_to_user_model.py
│       ├── fca21b76a184_add_photo_url_to_webinar_registrants.py
│       ├── 0333e16b1b9d_add_notes_field_to_webinar_registrants.py
│       └── 714ef079d138_merge_heads.py
├── alembic.ini            # Alembic configuration
├── scripts/               # Database setup scripts
│   ├── init_db.py         # Database initialization
│   ├── create_superuser.py # Superuser creation script
│   ├── add_test_users.py  # Test users creation script
│   ├── add_sample_products.py # Sample product data script
│   ├── add_sample_webinars.py # Sample webinar data script
│   ├── add_sample_webinar_registrants.py # Sample registrant data script
│   ├── clear_and_add_registrants.py # Clear and add registrants script
│   ├── download_sample_photos.py # Download sample photos script
│   ├── check_env.py       # Environment configuration checker
│   ├── check_users.py     # User verification script
│   ├── test_auth.py       # Authentication testing script
│   ├── production_start.py # Production startup script
│   └── migrate/           # Database migration management
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # MVS Architecture documentation
│   ├── authentication.md  # Authentication documentation
│   ├── call_for_volunteers.md # Volunteer documentation
│   ├── file_upload.md     # File upload documentation
│   ├── image_storage.md   # Image storage documentation
│   ├── MIGRATION_GUIDE.md # Migration guide
│   ├── oppkey_development_plans.md # Development plans
│   ├── postgresql_install.md # PostgreSQL installation guide
│   ├── production_vs_development.md # Environment differences
│   └── images/            # Screenshots and documentation images
├── test_ai_demo.py        # AI demo testing script
├── test_formatting.py     # Formatting testing script
├── test.db                # SQLite database (auto-created)
├── test.db.20250805_131918 # Database backup
├── .env                   # Environment variables (create this)
├── .gitignore             # Git ignore file
├── .python-version        # Python version specification
├── pyproject.toml         # Project dependencies
└── uv.lock                # Lock file
```

## Layer Responsibilities

### 1. Model Layer (`models.py`)
- **Purpose**: Define data structures and database models
- **Responsibilities**:
  - SQLModel/SQLAlchemy model definitions
  - Data validation and constraints
  - Database schema representation

### 2. View Layer (`routes/`)
- **Purpose**: Handle HTTP requests and responses
- **Responsibilities**:
  - Route definitions and HTTP method handling
  - Request/response formatting
  - Input validation
  - Authentication checks
  - Error handling

#### Route Modules:
- **`pages.py`**: HTML page rendering routes
- **`auth.py`**: Authentication and session management
- **`api.py`**: JSON API endpoints for data
- **`webinar.py`**: Webinar registrant management operations

### 3. Service Layer (`services/`)
- **Purpose**: Business logic and data operations
- **Responsibilities**:
  - Database operations
  - File handling
  - Business rules implementation
  - Data transformation
  - Error handling for business logic

#### Service Classes:
- **`ProductService`**: Product-related operations and statistics
- **`WebinarService`**: Webinar registrant management operations

## Benefits of This Architecture

### 1. **Separation of Concerns**
- Routes handle HTTP concerns only
- Services contain business logic
- Models focus on data structure

### 2. **Maintainability**
- Smaller, focused files (50-100 lines each vs 552 lines)
- Clear responsibility boundaries
- Easier to locate and modify specific functionality

### 3. **Testability**
- Services can be unit tested independently
- Routes can be tested with mocked services
- Clear interfaces between layers

### 4. **Reusability**
- Services can be used by multiple routes
- Business logic is centralized
- Consistent error handling

### 5. **Scalability**
- Easy to add new route modules
- Services can be extended without affecting routes
- Clear patterns for new features

## Migration Guide

### From `main_old.py` to `main.py`

The original `main.py` contained:
- **552 lines** of mixed responsibilities
- Database operations in route handlers
- File handling logic in routes
- Business logic scattered throughout

The new structure:
- **Routes**: 20-50 lines each, focused on HTTP handling
- **Services**: 50-100 lines each, focused on business logic
- **Main**: 60 lines, focused on app configuration

### Key Changes

1. **Route Organization**:
   ```python
   # Before: All routes in main.py
   @app.get("/")
   @app.post("/login")
   @app.get("/api/products")
   
   # After: Organized by responsibility
   # routes/pages.py
   @router.get("/")
   
   # routes/auth.py
   @router.post("/login")
   
   # routes/api.py
   @router.get("/products")
   ```

2. **Service Layer**:
   ```python
   # Before: Database logic in routes
   async def get_products():
       async with AsyncSessionLocal() as session:
           result = await session.execute(select(Product))
           # ... 50+ lines of business logic
   
   # After: Clean route with service call
   async def get_products():
       data = await ProductService.get_products_with_stats()
       return JSONResponse(data)
   ```

3. **Error Handling**:
   ```python
   # Before: Mixed error handling in routes
   try:
       # business logic
   except Exception as e:
       return HTMLResponse(f"Error: {str(e)}")
   
   # After: Consistent service error handling
   success, message = await WebinarService.update_notes(id, notes)
   if success:
       return success_response(message)
   else:
       return error_response(message)
   ```

## Usage

### Running the Application

```bash
# Run the application
python main.py

# Or with uvicorn
uvicorn main:app --reload
```

### Adding New Features

1. **New Route**: Add to appropriate route module
2. **New Service**: Create new service class in `services/`
3. **New Model**: Add to `models.py`

### Example: Adding a New Feature

```python
# 1. Add service method
# services/webinar_service.py
@staticmethod
async def get_registrant_by_id(registrant_id: str):
    # Business logic here
    pass

# 2. Add route
# routes/webinar.py
@router.get("/registrant/{registrant_id}")
async def get_registrant(registrant_id: str):
    registrant = await WebinarService.get_registrant_by_id(registrant_id)
    return JSONResponse(registrant)
```

## Best Practices

1. **Keep routes thin**: Routes should only handle HTTP concerns
2. **Use services for business logic**: All database/file operations go in services
3. **Consistent error handling**: Use service return tuples for success/error
4. **Clear naming**: Use descriptive names for routes and services
5. **Documentation**: Add docstrings to all public methods

## Future Enhancements

1. **Repository Pattern**: Add data access layer between services and models
2. **Dependency Injection**: Use FastAPI's dependency injection for services
3. **Validation Layer**: Add Pydantic models for request/response validation
4. **Caching Layer**: Add Redis or similar for caching
5. **Event System**: Add async event handling for side effects 