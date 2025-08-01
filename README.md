# FastOpp

FastAPI Oppkey starter package using pre-built admin
components to give FastAPI functionality comparable to Django.

The project is designed for Oppkey management (Jesse and Craig)
to assess FastAPI functionality.

The pre-built admin tools for FastAPI do not appear to be a
best practice or even popular among FastAPI developers.

After building applications with pre-built admin components, Oppkey
may eventually move from pre-built components to building
our own admin tools.

The tools could be a step in the process to evaluate FastAPI
or where Oppkey ends up.

```mermaid
flowchart TD
    A[FastOpp Assessment]
    A --> B[FastAPI+Pre-Built Admin]
    A --> C[FastAPI+Custom Admin]
    A --> D[Django with async, HTMX]
    A --> E[Django+FastAPI for LLM]
```

## Components

| Functional Concept| Component | Django Equivalent |
| -- | -- | -- |
| Production Web Server | FastAPI | NGINX  |
| Development Web Server | uvicorn  | `manage.py runserver` in development. Django Framework |
| Development SQL Database | SQLite | SQLite |
| Production SQL Database | PostgreSQL with pgvector | PostgreSQL with pgvector |
| User Management | [FastAPI Users](https://github.com/fastapi-users/fastapi-users) | Django Admin |
| Database Management | [SQLAdmin](https://aminalaee.github.io/sqladmin/) + Template | Django Admin |
| Authentication | Custom JWT + Session Auth (with database user verification and FastAPI Users password hashing) | Django Admin Auth |

## Project structure

```text
├── main.py                 # FastAPI application with routes
├── auth.py                 # JWT authentication system
├── admin_auth.py           # SQLAdmin authentication backend
├── templates/index.html    # Jinja2 templates
├── db.py                   # Database configuration
├── models.py               # SQLModel models
├── users.py                # FastAPI Users configuration
├── oppman.py               # Management tool for database operations
├── scripts/                # Database setup scripts
│   ├── init_db.py          # Database initialization
│   ├── create_superuser.py # Superuser creation script
│   ├── add_test_users.py   # Test users creation script
│   └── add_sample_products.py # Sample product data script
├── test.db                 # SQLite database (auto-created)
├── pyproject.toml          # Project dependencies
└── uv.lock                 # Lock file
```

## Quick Start

For a complete setup and start in one go:

```bash
# Install dependencies
uv sync

# Initialize everything and start server
uv run python oppman.py init
uv run python oppman.py runserver
```

Then visit:

- **Homepage**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/` (login: `admin@example.com / admin123`)
- **API Docs**: `http://localhost:8000/docs`

## Setup

```bash
uv sync
```

### 2. Initialize Database and Add Data

**Option A: Full Setup (Recommended)**

```bash
uv run python oppman.py init
```

This single command will:

- Initialize the database
- Create superuser: `admin@example.com` / `admin123`
- Add test users (password: `test123`)
- Add sample products

**Option B: Step-by-Step Setup**

```bash
# Initialize database
uv run python oppman.py db

# Create superuser
uv run python oppman.py superuser

# Add test users (optional)
uv run python oppman.py users

# Add sample products (optional)
uv run python oppman.py products
```

**Database Management**

```bash
# Backup current database
uv run python oppman.py backup

# Delete database (with automatic backup)
uv run python oppman.py delete

# Show help
uv run python oppman.py help
```

### 5. Start the Application

**Option A: Using Management Tool (Recommended)**

```bash
# Start server
uv run python oppman.py runserver

# Stop server
uv run python oppman.py stopserver
```

**Option B: Direct Command**

```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Authentication System

This FastAPI application includes a comprehensive authentication system with both web-based and API authentication. We use a **hybrid approach** that combines:

- **[FastAPI Users](https://github.com/fastapi-users/fastapi-users)** for password hashing and user management
- **Custom JWT authentication** for API access
- **Custom session-based authentication** for the admin panel

### Why This Approach?

We initially tried to use FastAPI Users' built-in authentication, but encountered compatibility issues with version 14.0.1. Instead, we built a custom authentication system that leverages FastAPI Users' excellent password hashing and user management features while providing our own JWT and session authentication.

### Admin Panel Authentication

The admin panel uses session-based authentication similar to Django's admin interface. **Authentication now verifies users against the database** instead of using hardcoded credentials.

#### Access Admin Panel

1. **Visit**: http://localhost:8000/admin/
2. **Login with any superuser account**:
   - Username: `admin@example.com` (or any other superuser email)
   - Password: `admin123` (or the actual password for that user)

#### Features

- ✅ **Session-based authentication**
- ✅ **Secure password verification**
- ✅ **Superuser permission checking**
- ✅ **Database user lookup**
- ✅ **User management interface**

### API Authentication

The application provides JWT-based authentication for API access.

#### Get Authentication Token

```bash
curl -X POST http://localhost:8000/login \
  -u "admin@example.com:admin123" \
  -H "Content-Type: application/json"
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Use Token for API Calls

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  http://localhost:8000/admin/
```

### Authentication Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/` | GET | Homepage | No |
| `/admin/` | GET | Admin panel | Yes (Session) |
| `/login` | POST | Get JWT token | Basic Auth |
| `/docs` | GET | API documentation | No |

## Available Features

### 1. **Management Tool** (`oppman.py`)
- Complete database initialization with one command
- Individual setup operations (database, users, products)
- Development server management (start/stop with `--reload`)
- Production server with Gunicorn (no Nginx required)
- Database backup and deletion with automatic backups
- Comprehensive help system
- Test data creation for development

### 2. **Admin Panel** (`http://localhost:8000/admin/`)

- Django-like admin interface
- User management (create, edit, delete)
- Product management (create, edit, delete)
- Database record management
- Session-based authentication

### 2. **API Documentation** (`http://localhost:8000/docs`)

- Interactive Swagger UI
- Auto-generated from FastAPI code
- Test endpoints directly

### 3. **User Management**

- User registration and authentication
- Password hashing with [FastAPI Users](https://github.com/fastapi-users/fastapi-users)
- Superuser permissions
- Active/inactive user status

### 4. **Database Integration**

- SQLModel ORM (Pydantic + SQLAlchemy)
- SQLite for development
- Async database operations
- Alembic migrations support
- Multiple model support (Users, Products, etc.)

## Security Features

- ✅ **JWT token authentication** for APIs (custom implementation)
- ✅ **Session-based authentication** for admin panel (custom implementation)
- ✅ **Password hashing** with Argon2 (via FastAPI Users)
- ✅ **Superuser permission checking**
- ✅ **Database user verification**
- ✅ **Secure session management**

## Development

### Code Quality Checks

```bash
# Type checking with mypy
uv run mypy db.py
uv run mypy main.py
uv run mypy auth.py

# Linting with ruff
uv run ruff check db.py
uv run ruff check main.py
uv run ruff check auth.py
```

### Adding New Models

1. **Define model** in `models.py` (see Product model example)
2. **Create admin view** in `main.py` (see ProductAdmin example)
3. **Run database migration** (if using Alembic)
4. **Add sample data** (optional, see `add_sample_products.py`)

### Customizing Authentication

The authentication system is modular:

- **`auth.py`**: Custom JWT token authentication
- **`admin_auth.py`**: Custom SQLAdmin authentication backend
- **`main.py`**: Login endpoints and admin configuration
- **`users.py`**: FastAPI Users configuration (for password hashing)

## Production Considerations

1. **Change default secrets**:
   - Update `SECRET_KEY` in `auth.py`
   - Update session secret in `main.py`

2. **Use environment variables**:

   ```python
   import os
   SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
   ```

3. **Database**: Switch from SQLite to PostgreSQL
4. **HTTPS**: Configure SSL/TLS certificates
5. **Rate limiting**: Add request rate limiting
6. **Logging**: Configure proper logging

## Troubleshooting

### Common Issues

1. **Module not found errors**: Run `uv sync` to install dependencies
2. **Database errors**: Run `uv run python init_db.py` to recreate database
3. **Authentication fails**: Check if superuser exists with `uv run python create_superuser.py`
4. **Port already in use**: Change port with `--port 8001`

### Reset Database

```bash
# Option A: Using management tool (recommended)
uv run python oppman.py delete
uv run python oppman.py init

# Option B: Manual reset
rm test.db
uv run python oppman.py db
uv run python oppman.py superuser
uv run python oppman.py users
uv run python oppman.py products
```

## Resources

- [PostgreSQL Install for Production](docs/postgresql_install.md)
- [Production versus Development](docs/production_vs_development.md)
