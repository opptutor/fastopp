# FastOpp

FastAPI Oppkey starter package using pre-built admin
components to give FastAPI functionality comparable to Django.

## Screenshots

### Interactive

![home](docs/images/home.webp)

![interactive](docs/images/interactive.webp)

### Cards with Mouseover

![cards](docs/images/cards.webp)

### Hero

![hero](docs/images/hero.webp)

### Database Admin List

![admin list](docs/images/admin.webp)

### Database Entry Edit

![edit](docs/images/edit.webp)

### User Management

![user management](docs/images/user_management.webp)

### User Authentication

Admin panel is restricted to logged-in users.

![authentication](docs/images/login.webp)

### Statistics Hero Card

![webinar top](docs/images/webinar_top.webp)

### People Hero Card

![webinar people](docs/images/webinar_people.webp)

### AI Chat

![AI Chat](docs/images/ai_chat.webp)

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

## Project structure

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
├── auth.py                # JWT authentication system
├── admin_auth.py          # SQLAdmin authentication backend
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
├── users.py               # FastAPI Users configuration
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

## 🚀 Quick Start (For Team Members)

### Prerequisites

- Python 3.12+
  If Python 3.12+ is not on your Mac, consider [installing pyenv](https://youtu.be/1F2IK7CU76U?feature=shared)
  and install the newest 3.12.x with pyenv. Although the latest stable Python is 3.13.5, we're using 3.12.x
  right now for maximum package compatibility.
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd fastopp

# Install dependencies
uv sync

# Add environment variable support
uv add python-dotenv
```

### 2. Environment Configuration

Create a `.env` file in your project root:

**Required Environment Variables:**

- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT tokens and session management
- `ENVIRONMENT`: Set to "development" for development mode
- `OPENROUTER_API_KEY`: API key for OpenRouter (required for AI demo features)

```bash
# Create environment file with secure defaults
cat > .env << EOF
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=dev_secret_key_$(openssl rand -hex 32)
ENVIRONMENT=development
OPENROUTER_API_KEY=your_openrouter_api_key_here
EOF
```

**Or manually create `.env`:**

```bash
# .env
DATABASE_URL=sqlite+aiosqlite:///./test.db
SECRET_KEY=dev_secret_key_change_in_production_$(openssl rand -hex 32)
ENVIRONMENT=development
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. One-Command Setup

```bash
# Complete setup with one command
uv run python oppman.py init
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
uv run python oppman.py migrate init

# Create initial migration
uv run python oppman.py migrate create "Initial migration"

# Apply migrations
uv run python oppman.py migrate upgrade

# Initialize database with sample data
uv run python oppman.py init
```

### 4. Start Development Server

```bash
# Start the server
uv run python oppman.py runserver
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

## 🛠️ Management Commands

### Database Operations

```bash
# Initialize everything (database + superuser + users + products)
uv run python oppman.py init

# Individual operations
uv run python oppman.py db              # Initialize database only
uv run python oppman.py superuser       # Create superuser only
uv run python oppman.py users           # Add test users only
uv run python oppman.py products        # Add sample products only

# Database management
uv run python oppman.py backup          # Backup database
uv run python oppman.py delete          # Delete database (with backup)
```

### Server Management

```bash
# Development server
uv run python oppman.py runserver       # Start development server
uv run python oppman.py stopserver      # Stop development server

# Production server (optional)
uv run python oppman.py production      # Start production server
```

### Migration Management

```bash
# Initialize migrations (first time only)
uv run python oppman.py migrate init

# Create new migration
uv run python oppman.py migrate create "Add new table"

# Apply migrations
uv run python oppman.py migrate upgrade

# Check migration status
uv run python oppman.py migrate current

# View migration history
uv run python oppman.py migrate history
```

### Environment Management

```bash
# Check environment configuration
uv run python oppman.py env

# Show all available commands
uv run python oppman.py help
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
2. **Create Migration**: `uv run python oppman.py migrate create "Description"`
3. **Review Migration**: Check the generated file in `alembic/versions/`
4. **Apply Migration**: `uv run python oppman.py migrate upgrade`
5. **Verify**: `uv run python oppman.py migrate current`

## 🚨 Troubleshooting

### Common Issues

1. **"Alembic not found"**

   ```bash
   uv add alembic
   ```

2. **"Alembic not initialized"**

   ```bash
   uv run python oppman.py migrate init
   ```

3. **Environment issues**
 
     ```bash
     # Check environment configuration
     uv run python oppman.py env
     ```

4. **Database issues**
 
     ```bash
     # Backup and reset
     uv run python oppman.py backup
     uv run python oppman.py delete
     uv run python oppman.py init
     ```

5. **"Module not found" errors**

   ```bash
   # Reinstall dependencies
   uv sync
   ```

6. **Port already in use**
 
     ```bash
     # Stop any running servers
     uv run python oppman.py stopserver
     
     # Or use a different port
     uv run uvicorn main:app --reload --port 8001
     ```

### Quick Reset

If something goes wrong, you can reset everything:

```bash
# Backup current database
uv run python oppman.py backup

# Delete and reinitialize
uv run python oppman.py delete
uv run python oppman.py init

# Verify setup
uv run python oppman.py env
```

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md) - MVS Architecture and code organization
- [PostgreSQL Installation Guide](docs/postgresql_install.md) - Database setup for production
- [Production vs Development](docs/production_vs_development.md) - Environment differences
- [Migration Guide](docs/MIGRATION_GUIDE.md) - Database migration management
- [Authentication System](docs/authentication.md) - Authentication and authorization details
- [Oppkey Development Plans](docs/oppkey_development_plans.md) - includes assessment plans
