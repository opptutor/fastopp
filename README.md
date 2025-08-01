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
├── db.py                   # Database configuration (uses environment variables)
├── models.py               # SQLModel models
├── users.py                # FastAPI Users configuration
├── oppman.py               # Management tool for database operations
├── scripts/                # Database setup scripts
│   ├── init_db.py          # Database initialization
│   ├── create_superuser.py # Superuser creation script
│   ├── add_test_users.py   # Test users creation script
│   ├── add_sample_products.py # Sample product data script
│   ├── check_env.py        # Environment configuration checker
│   └── migrate/            # Database migration management
├── test.db                 # SQLite database (auto-created)
├── .env                    # Environment variables (create this)
├── pyproject.toml          # Project dependencies
└── uv.lock                 # Lock file
```

## 🚀 Quick Start (For Team Members)

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd fastapi_d

# Install dependencies
uv sync

# Add environment variable support
uv add python-dotenv
```

### 2. Environment Configuration

Create a `.env` file in your project root:

```bash
# Create environment file with secure defaults
cat > .env << EOF
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=dev_secret_key_$(openssl rand -hex 32)
ENVIRONMENT=development
EOF
```

**Or manually create `.env`:**

```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=dev_secret_key_change_in_production_$(openssl rand -hex 32)
ENVIRONMENT=development
```

### 3. One-Command Setup

```bash
# Complete setup with one command
python oppman.py init
```

This single command will:
- Initialize migrations
- Create initial migration
- Apply migrations
- Initialize database with sample data
- Create superuser and test data

**Alternative: Step-by-Step Setup**

If you prefer to understand each step:

```bash
# Initialize migrations (first time only)
python oppman.py migrate init

# Create initial migration
python oppman.py migrate create "Initial migration"

# Apply migrations
python oppman.py migrate upgrade

# Initialize database with sample data
python oppman.py init
```

### 4. Start Development Server

```bash
# Start the server
python oppman.py runserver
```

### 5. Access the Application

Visit these URLs in your browser:

- **Homepage**: `http://localhost:8000/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **API Docs**: `http://localhost:8000/docs`

#### Admin Panel Login

Use these credentials to access the admin panel:

- **Email**: `admin@example.com`
- **Password**: `admin123`

## 🔧 Environment Configuration

The project uses environment variables for flexible configuration:

### Development Setup (Default)

```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=dev_secret_key_change_in_production_$(openssl rand -hex 32)
ENVIRONMENT=development
```

### Production Setup (Optional)

```bash
# .env (production)
DATABASE_URL=postgresql+asyncpg://user:password@localhost/fastopp_db
SECRET_KEY=your_very_secure_production_secret_key_here
ENVIRONMENT=production
```

### Check Environment Configuration

```bash
# Verify your environment setup
python oppman.py env
```

## 🛠️ Management Commands

### Database Operations

```bash
# Initialize everything (database + superuser + users + products)
python oppman.py init

# Individual operations
python oppman.py db              # Initialize database only
python oppman.py superuser       # Create superuser only
python oppman.py users           # Add test users only
python oppman.py products        # Add sample products only

# Database management
python oppman.py backup          # Backup database
python oppman.py delete          # Delete database (with backup)
```

### Server Management

```bash
# Development server
python oppman.py runserver       # Start development server
python oppman.py stopserver      # Stop development server

# Production server (optional)
python oppman.py production      # Start production server
```

### Migration Management

```bash
# Initialize migrations (first time only)
python oppman.py migrate init

# Create new migration
python oppman.py migrate create "Add new table"

# Apply migrations
python oppman.py migrate upgrade

# Check migration status
python oppman.py migrate current

# View migration history
python oppman.py migrate history
```

### Environment Management

```bash
# Check environment configuration
python oppman.py env

# Show all available commands
python oppman.py help
```

## 🔐 Authentication System

This FastAPI application includes a comprehensive authentication system with both web-based and API authentication. We use a **hybrid approach** that combines:

- **[FastAPI Users](https://github.com/fastapi-users/fastapi-users)** for password hashing and user management
- **Custom JWT authentication** for API access
- **Custom session-based authentication** for the admin panel

### Admin Panel Authentication

The admin panel uses session-based authentication similar to Django's admin interface. **Authentication verifies users against the database** instead of using hardcoded credentials.

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
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Use Authentication Token

```bash
curl -X GET http://localhost:8000/admin/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## 📊 Test Data

The application comes with pre-loaded test data:

### Users

- **Superuser**: `admin@example.com` / `admin123`
- **Test Users**: `john@example.com`, `jane@example.com`, `bob@example.com` / `test123`

### Products

Sample products with various categories and prices for testing the admin interface.

## 🔄 Database Migrations

The project uses Alembic for database migrations, providing Django-like migration functionality:

### Migration Workflow

1. **Add/Modify Models**: Edit `models.py` with your changes
2. **Create Migration**: `python oppman.py migrate create "Description"`
3. **Review Migration**: Check the generated file in `alembic/versions/`
4. **Apply Migration**: `python oppman.py migrate upgrade`
5. **Verify**: `python oppman.py migrate current`

### Migration Commands

```bash
# Initialize migrations (first time only)
python oppman.py migrate init

# Create a new migration
python oppman.py migrate create "Add user profile table"

# Apply all pending migrations
python oppman.py migrate upgrade

# Check current status
python oppman.py migrate current

# View migration history
python oppman.py migrate history
```

## 🚨 Troubleshooting

### Common Issues

1. **"Alembic not found"**
   ```bash
   uv add alembic
   ```

2. **"Alembic not initialized"**
   ```bash
   python oppman.py migrate init
   ```

3. **Environment issues**
   ```bash
   # Check environment configuration
   python oppman.py env
   ```

4. **Database issues**
   ```bash
   # Backup and reset
   python oppman.py backup
   python oppman.py delete
   python oppman.py init
   ```

5. **"Module not found" errors**
   ```bash
   # Reinstall dependencies
   uv sync
   ```

6. **Port already in use**
   ```bash
   # Stop any running servers
   python oppman.py stopserver
   
   # Or use a different port
   uv run uvicorn main:app --reload --port 8001
   ```

### Quick Reset

If something goes wrong, you can reset everything:

```bash
# Backup current database
python oppman.py backup

# Delete and reinitialize
python oppman.py delete
python oppman.py init

# Verify setup
python oppman.py env
```

### Environment Variables

- ✅ **Never commit `.env` files** to version control
- ✅ **Use different secret keys** for development and production
- ✅ **Use strong, random secret keys** in production
- ✅ **Environment variables** keep credentials out of source code

## 📚 Documentation

- [PostgreSQL Installation Guide](docs/postgresql_install.md) - Database setup for production
- [Production vs Development](docs/production_vs_development.md) - Environment differences
- [Migration Guide](docs/MIGRATION_GUIDE.md) - Database migration management

## 🎯 Evaluation Focus

This setup allows your team to quickly evaluate:

1. **FastAPI Admin Interface** - Compare with Django Admin
2. **Authentication System** - JWT + Session-based auth
3. **Database Management** - SQLModel + Alembic migrations
4. **Development Experience** - Environment variables, management commands
5. **Production Readiness** - PostgreSQL, Gunicorn, environment config

The goal is to assess whether FastAPI + pre-built admin tools can provide a Django-like development experience for your team.
