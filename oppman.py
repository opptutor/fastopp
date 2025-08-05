#!/usr/bin/env python3
"""
Oppkey Management Tool (oppman.py)
A comprehensive tool for managing the FastAPI admin application.
"""
import argparse
import asyncio
import os
import shutil
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# Add the current directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from scripts.init_db import init_db
    from scripts.create_superuser import create_superuser
    from scripts.add_test_users import add_test_users
    from scripts.add_sample_products import add_sample_products
    from scripts.add_sample_webinars import add_sample_webinars
    from scripts.add_sample_webinar_registrants import add_sample_registrants
    from scripts.clear_and_add_registrants import clear_and_add_registrants
    from scripts.download_sample_photos import download_sample_photos
    from scripts.check_users import check_users
    from scripts.test_auth import test_auth
    from scripts.migrate.cli import run_migrate_command, show_migration_help
    from scripts.check_env import check_environment
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts/ directory")
    sys.exit(1)


def backup_database():
    """Backup the current database with timestamp"""
    db_path = Path("test.db")
    if not db_path.exists():
        print("❌ No database file found to backup")
        return False
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(f"test.db.{timestamp}")
    
    try:
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Failed to backup database: {e}")
        return False


def delete_database():
    """Delete the current database file"""
    db_path = Path("test.db")
    if not db_path.exists():
        print("❌ No database file found to delete")
        return False
    
    try:
        # Backup first
        if backup_database():
            db_path.unlink()
            print("✅ Database deleted successfully")
            return True
        else:
            print("❌ Failed to backup database, not deleting")
            return False
    except Exception as e:
        print(f"❌ Failed to delete database: {e}")
        return False


async def run_init():
    """Initialize a new database"""
    print("🔄 Initializing database...")
    await init_db()
    print("✅ Database initialization complete")


async def run_superuser():
    """Create superuser"""
    print("🔄 Creating superuser...")
    await create_superuser()
    print("✅ Superuser creation complete")


async def run_users():
    """Add test users"""
    print("🔄 Adding test users...")
    await add_test_users()
    print("✅ Test users creation complete")


async def run_products():
    """Add sample products"""
    print("🔄 Adding sample products...")
    await add_sample_products()
    print("✅ Sample products creation complete")


async def run_webinars():
    """Add sample webinars"""
    print("🔄 Adding sample webinars...")
    await add_sample_webinars()
    print("✅ Sample webinars creation complete")


async def run_download_photos():
    """Download sample photos for webinar registrants"""
    print("🔄 Downloading sample photos...")
    download_sample_photos()
    print("✅ Sample photos download complete")


async def run_registrants():
    """Add sample webinar registrants with photos"""
    print("🔄 Adding sample webinar registrants...")
    await add_sample_registrants()
    print("✅ Sample webinar registrants creation complete")


async def run_clear_registrants():
    """Clear and add fresh webinar registrants with photos"""
    print("🔄 Clearing and adding fresh webinar registrants...")
    await clear_and_add_registrants()
    print("✅ Fresh webinar registrants creation complete")


async def run_check_users():
    """Check existing users and their permissions"""
    print("🔄 Checking users...")
    await check_users()
    print("✅ User check complete")


async def run_test_auth():
    """Test the authentication system"""
    print("🔄 Testing authentication system...")
    await test_auth()
    print("✅ Authentication test complete")


def run_server():
    """Start the development server with uvicorn"""
    print("🚀 Starting development server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔧 Admin panel: http://localhost:8000/admin/")
    print("📚 API docs: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start uvicorn with reload
        subprocess.run([
            "uv", "run", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def stop_server():
    """Stop the development server"""
    print("🛑 Stopping development server...")
    
    try:
        # Kill uvicorn processes
        result = subprocess.run([
            "pkill", "-f", "uv run uvicorn main:app"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Development server stopped successfully")
            return True
        else:
            print("ℹ️  No development server found running")
            return True
    except Exception as e:
        print(f"❌ Failed to stop server: {e}")
        return False


def run_production_server():
    """Start the production server with Gunicorn"""
    print("🚀 Starting FastAPI production server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔧 Admin panel: http://localhost:8000/admin/")
    print("📚 API docs: http://localhost:8000/docs")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    try:
        # Start gunicorn with uvicorn workers
        subprocess.run([
            "uv", "run", "gunicorn",
            "main:app",
            "-w", "4",  # 4 workers
            "-k", "uvicorn.workers.UvicornWorker",
            "--bind", "0.0.0.0:8000",
            "--timeout", "120",
            "--keep-alive", "5",
            "--max-requests", "1000",
            "--max-requests-jitter", "50"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start server: {e}")
        print("Make sure asyncpg and gunicorn are installed: uv add asyncpg gunicorn")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


async def run_full_init():
    """Run complete initialization: init + superuser + users + products + webinars + registrants"""
    print("🚀 Running full initialization...")
    
    await run_init()
    await run_superuser()
    await run_users()
    await run_products()
    await run_webinars()
    await run_download_photos()
    await run_registrants()
    await run_clear_registrants()
    
    print("✅ Full initialization complete!")
    print("\n📋 Summary:")
    print("- Database initialized")
    print("- Superuser created: admin@example.com / admin123")
    print("- Test users added (password: test123)")
    print("- Sample products added")
    print("- Sample webinars added")
    print("- Sample photos downloaded")
    print("- Webinar registrants added with photos")
    print("\n🌐 Ready to start the application with: uv run uvicorn main:app --reload")
    print("🔐 Login to webinar registrants: http://localhost:8000/webinar-registrants")


def show_help():
    """Show detailed help information"""
    help_text = """
Oppkey Management Tool (oppman.py)

A comprehensive tool for managing the FastAPI admin application.

USAGE:
    python oppman.py <command> [options]

COMMANDS:
    init        Complete initialization (database + superuser + users + products + webinars + registrants)
    db          Initialize database only
    superuser   Create superuser only
    users       Add test users only
    products    Add sample products only
    webinars    Add sample webinars only
    download_photos  Download sample photos for webinar registrants
    registrants Add sample webinar registrants with photos
    clear_registrants Clear and add fresh webinar registrants with photos
    check_users Check existing users and their permissions
    test_auth   Test the authentication system
    runserver   Start development server with uvicorn --reload
    stopserver  Stop development server
    production  Start production server with Gunicorn (no Nginx)
    delete      Delete current database (with backup)
    backup      Backup current database
    migrate     Database migration management (see examples below)
    env         Check environment configuration
    help        Show this help message

EXAMPLES:
    # Full initialization (recommended for first-time setup)
    python oppman.py init
    
    # Individual operations
    python oppman.py db
    python oppman.py superuser
    python oppman.py users
    python oppman.py products
    python oppman.py webinars
    python oppman.py download_photos
    python oppman.py registrants
    python oppman.py clear_registrants
    python oppman.py check_users
    python oppman.py test_auth
    
    # Start development server
    python oppman.py runserver
    
    # Stop development server
    python oppman.py stopserver
    
    # Start production server (no Nginx)
    python oppman.py production
    
    # Database management
    python oppman.py backup
    python oppman.py delete
    
    # Migration management
    python oppman.py migrate init
    python oppman.py migrate create "Add new table"
    python oppman.py migrate upgrade
    python oppman.py migrate current
    
    # Environment management
    python oppman.py env

DEFAULT CREDENTIALS:
    Superuser: admin@example.com / admin123
    Test Users: test123 (for all test users)
    
    Test Users Created:
    - admin@example.com (superuser, admin)
    - admin2@example.com (superuser, admin)
    - john@example.com (staff, marketing)
    - jane@example.com (staff, sales)
    - staff@example.com (staff, support)
    - marketing@example.com (staff, marketing)
    - sales@example.com (staff, sales)
    - bob@example.com (inactive)

PERMISSION LEVELS:
    - Superusers: Full admin access (users + products + webinars + audit)
    - Marketing: Product management + webinar management
    - Sales: Product management + assigned webinar viewing
    - Support: Product management only
    - Regular users: No admin access

WEBINAR REGISTRANTS:
    - Access: http://localhost:8000/webinar-registrants
    - Login required: Staff or admin access
    - Features: Photo upload, registrant management
    - Sample data: 5 registrants with professional photos
    - Commands: download_photos, registrants, clear_registrants

DATABASE:
    - Development: SQLite (test.db)
    - Backup format: test.db.YYYYMMDD_HHMMSS

SERVER:
    - Development server: http://localhost:8000
    - Admin panel: http://localhost:8000/admin/
    - API docs: http://localhost:8000/docs
    - Webinar registrants: http://localhost:8000/webinar-registrants
    """
    print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Oppkey Management Tool for FastAPI Admin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python oppman.py init      # Full initialization
  python oppman.py db        # Initialize database only
  python oppman.py delete    # Delete database with backup
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "init", "db", "superuser", "users", "products", "webinars",
            "download_photos", "registrants", "clear_registrants", "check_users", "test_auth",
            "runserver", "stopserver", "production", "delete", "backup", "migrate", "env", "help"
        ],
        help="Command to execute"
    )
    
    parser.add_argument(
        "migrate_command",
        nargs="?",
        help="Migration subcommand (use with 'migrate')"
    )
    
    parser.add_argument(
        "migrate_args",
        nargs="*",
        help="Additional arguments for migration command"
    )
    
    args = parser.parse_args()
    
    # If no command provided, show help
    if not args.command:
        show_help()
        return
    
    # Handle help command
    if args.command == "help":
        show_help()
        return
    
    # Handle non-async commands
    if args.command == "delete":
        delete_database()
        return
    
    if args.command == "backup":
        backup_database()
        return
    
    if args.command == "runserver":
        run_server()
        return
    
    if args.command == "stopserver":
        stop_server()
        return
    
    if args.command == "production":
        run_production_server()
        return
    
    if args.command == "migrate":
        if not args.migrate_command:
            show_migration_help()
            return
        
        success = run_migrate_command(args.migrate_command, args.migrate_args)
        if not success:
            sys.exit(1)
        return
    
    if args.command == "env":
        check_environment()
        return
    
    # Handle async commands
    async def run_command():
        if args.command == "init":
            await run_full_init()
        elif args.command == "db":
            await run_init()
        elif args.command == "superuser":
            await run_superuser()
        elif args.command == "users":
            await run_users()
        elif args.command == "products":
            await run_products()
        elif args.command == "webinars":
            await run_webinars()
        elif args.command == "download_photos":
            await run_download_photos()
        elif args.command == "registrants":
            await run_registrants()
        elif args.command == "clear_registrants":
            await run_clear_registrants()
        elif args.command == "check_users":
            await run_check_users()
        elif args.command == "test_auth":
            await run_test_auth()
    
    # Run the async command
    asyncio.run(run_command())


if __name__ == "__main__":
    main() 