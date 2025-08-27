#!/usr/bin/env python3
"""
Oppkey Management Tool (oppman.py)
A core tool for managing database migrations, user management, and application setup.
Demo commands have been moved to oppdemo.py for better separation of concerns.
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
    from scripts.change_password import list_users, change_password_interactive
    from scripts.migrate.cli import run_migrate_command, show_migration_help
    from scripts.check_env import check_environment
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts/ directory")
    sys.exit(1)


def ensure_upload_dirs():
    """Ensure static upload directories exist regardless of current working directory."""
    project_root = Path(__file__).resolve().parent
    uploads_root = project_root / "static" / "uploads"
    photos_dir = uploads_root / "photos"
    sample_photos_dir = uploads_root / "sample_photos"
    uploads_root.mkdir(parents=True, exist_ok=True)
    photos_dir.mkdir(parents=True, exist_ok=True)
    sample_photos_dir.mkdir(parents=True, exist_ok=True)


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


def demo_command_help():
    """Show help message for demo commands that have been moved to oppdemo.py"""
    print("🔄 Demo commands have been moved to a new file: oppdemo.py")
    print()
    print("📋 Available demo file management commands:")
    print("   uv run python oppdemo.py save      # Save demo files")
    print("   uv run python oppdemo.py restore   # Restore demo files")
    print("   uv run python oppdemo.py destroy   # Switch to minimal app")
    print("   uv run python oppdemo.py diff      # Show differences")
    print("   uv run python oppdemo.py backups   # List all backups")
    print()
    print("📊 Available demo data initialization commands:")
    print("   uv run python oppdemo.py init      # Full initialization")
    print("   uv run python oppdemo.py db        # Initialize database only")
    print("   uv run python oppdemo.py superuser # Create superuser only")
    print("   uv run python oppdemo.py users     # Add test users only")
    print("   uv run python oppdemo.py products  # Add sample products only")
    print("   uv run python oppdemo.py webinars  # Add sample webinars only")
    print("   uv run python oppdemo.py download_photos  # Download sample photos")
    print("   uv run python oppdemo.py registrants      # Add sample registrants")
    print("   uv run python oppdemo.py clear_registrants # Clear and add fresh registrants")
    print("   uv run python oppdemo.py check_users      # Check existing users")
    print("   uv run python oppdemo.py test_auth        # Test authentication")
    print("   uv run python oppdemo.py change_password  # Change user password")
    print("   uv run python oppdemo.py list_users       # List all users")
    print()
    print("💡 For more information:")
    print("   uv run python oppdemo.py help")
    print()
    print("🔧 oppman.py now focuses on core database and application management.")
    print("📚 oppdemo.py handles all demo-related functionality.")


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


def backup_migrations() -> Path | None:
    """Backup Alembic migration files (alembic/versions) to a timestamped directory."""
    versions_dir = Path("alembic") / "versions"
    if not versions_dir.exists():
        print("❌ No alembic/versions directory found to backup")
        return None

    migration_files = [p for p in versions_dir.glob("*.py") if p.is_file()]
    if not migration_files:
        print("ℹ️  No migration files found to backup")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = Path("alembic") / f"versions_backup_{timestamp}"
    backup_root.mkdir(parents=True, exist_ok=True)

    try:
        for migration_file in migration_files:
            shutil.copy2(migration_file, backup_root / migration_file.name)
        print(f"✅ Migrations backed up to: {backup_root}")
        return backup_root
    except Exception as e:
        print(f"❌ Failed to backup migrations: {e}")
        return None


def delete_migration_files() -> bool:
    """Delete all Alembic migration .py files from alembic/versions and clean __pycache__."""
    versions_dir = Path("alembic") / "versions"
    if not versions_dir.exists():
        print("❌ No alembic/versions directory found")
        return False

    migration_files = [p for p in versions_dir.glob("*.py") if p.is_file()]
    if not migration_files:
        print("ℹ️  No migration files to delete")
        # Still attempt to remove __pycache__ if present
        pycache_dir = versions_dir / "__pycache__"
        if pycache_dir.exists():
            try:
                shutil.rmtree(pycache_dir)
                print("🧹 Removed alembic/versions/__pycache__")
            except Exception as e:
                print(f"⚠️  Failed to remove __pycache__: {e}")
        return True

    try:
        for migration_file in migration_files:
            migration_file.unlink()
        print("✅ Deleted migration files from alembic/versions")
        # Clean __pycache__ as well
        pycache_dir = versions_dir / "__pycache__"
        if pycache_dir.exists():
            try:
                shutil.rmtree(pycache_dir)
                print("🧹 Removed alembic/versions/__pycache__")
            except Exception as e:
                print(f"⚠️  Failed to remove __pycache__: {e}")
        return True
    except Exception as e:
        print(f"❌ Failed to delete migration files: {e}")
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
    ensure_upload_dirs()
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


async def run_change_password():
    """Change user password interactively"""
    print("🔐 Changing user password...")
    await change_password_interactive()


async def run_list_users():
    """List all users"""
    print("👥 Listing users...")
    await list_users()


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
    ensure_upload_dirs()
    
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

A core tool for managing database migrations, user management, and application setup.
Similar to Django's manage.py, this tool focuses on core application management.
Demo commands have been moved to oppdemo.py for better separation of concerns.

USAGE:
    uv run python oppman.py <command> [options]

COMMANDS:
    # Core application management
    runserver   Start development server with uvicorn --reload
    stopserver  Stop development server
    production  Start production server with Gunicorn (no Nginx)
    
    # Database management
    delete      Delete current database (with backup)
    backup      Backup current database
    migrate     Database migration management (see examples below)
    
    # Environment and utilities
    env         Check environment configuration
    demo        Demo commands have been moved to oppdemo.py
    help        Show this help message
    
    # Demo data initialization (DEPRECATED - use oppdemo.py instead)
    # These commands are deprecated and will be removed in a future version
    # Use 'uv run python oppdemo.py <command>' instead
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
    change_password Change user password interactively
    list_users  List all users in the database

EXAMPLES:
    # Core application management
    uv run python oppman.py runserver      # Start development server
    uv run python oppman.py stopserver     # Stop development server
    uv run python oppman.py production     # Start production server
    
    # Database management
    uv run python oppman.py backup         # Backup database
    uv run python oppman.py delete         # Delete database (with backup)
    uv run python oppman.py migrate init   # Initialize migrations
    uv run python oppman.py migrate create "Add new table"  # Create migration
    uv run python oppman.py migrate upgrade  # Apply migrations
    uv run python oppman.py migrate current  # Show current migration
    
    # Environment management
    uv run python oppman.py env            # Check environment configuration
    
    # Demo data initialization (DEPRECATED - use oppdemo.py instead)
    # These commands are deprecated and will be removed in a future version
    # Use 'uv run python oppdemo.py <command>' instead
    uv run python oppdemo.py init          # Full initialization
    uv run python oppdemo.py users         # Add test users
    uv run python oppdemo.py products      # Add sample products
    uv run python oppdemo.py webinars      # Add sample webinars
    uv run python oppdemo.py download_photos  # Download sample photos
    uv run python oppdemo.py registrants  # Add sample registrants
    uv run python oppdemo.py clear_registrants  # Clear and add fresh registrants
    uv run python oppdemo.py check_users  # Check existing users
    uv run python oppdemo.py test_auth    # Test authentication
    uv run python oppdemo.py change_password  # Change user password
    uv run python oppdemo.py list_users   # List all users
    
    # Demo file management (use oppdemo.py)
    uv run python oppdemo.py save          # Save demo files
    uv run python oppdemo.py restore       # Restore demo files
    uv run python oppdemo.py destroy       # Switch to minimal app
    uv run python oppdemo.py diff          # Show differences

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

PASSWORD MANAGEMENT:
    - change_password: Interactive password change for any user
    - list_users: View all users and their status
    - Usage: uv run python oppdemo.py change_password (DEPRECATED: use oppdemo.py)
    - Direct script: uv run python scripts/change_password.py --email user@example.com --password newpass

WEBINAR REGISTRANTS:
    - Access: http://localhost:8000/webinar-registrants
    - Login required: Staff or admin access
    - Features: Photo upload, registrant management
    - Sample data: 5 registrants with professional photos
    - Commands: download_photos, registrants, clear_registrants (DEPRECATED: use oppdemo.py)

DATABASE:
    - Development: SQLite (test.db)
    - Backup format: test.db.YYYYMMDD_HHMMSS

SERVER:
    - Development server: http://localhost:8000
    - Admin panel: http://localhost:8000/admin/
    - API docs: http://localhost:8000/docs
    - Webinar registrants: http://localhost:8000/webinar-registrants

NOTE: Demo data initialization commands are deprecated in oppman.py.
Use 'uv run python oppdemo.py <command>' instead for all demo-related functionality.
    """
    print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Oppkey Management Tool for FastAPI Admin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run python oppman.py init      # Full initialization
  uv run python oppman.py db        # Initialize database only
  uv run python oppman.py delete    # Delete database with backup
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            "init", "db", "superuser", "users", "products", "webinars",
            "download_photos", "registrants", "clear_registrants", "check_users", "test_auth",
            "change_password", "list_users",
            "runserver", "stopserver", "production", "delete", "backup", "demo", "migrate", "env", "help"
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
        # Delete database (with backup)
        delete_database()
        # Always attempt to backup and clean migrations regardless of DB deletion result
        backup_migrations()
        delete_migration_files()
        return
    
    if args.command == "backup":
        backup_database()
        return
    
    if args.command == "demo":
        demo_command_help()
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
            print("⚠️  DEPRECATION WARNING: 'oppman.py init' is deprecated.")
            print("   Use 'uv run python oppdemo.py init' instead.")
            print()
            await run_full_init()
        elif args.command == "db":
            print("⚠️  DEPRECATION WARNING: 'oppman.py db' is deprecated.")
            print("   Use 'uv run python oppdemo.py db' instead.")
            print()
            await run_init()
        elif args.command == "superuser":
            print("⚠️  DEPRECATION WARNING: 'oppman.py superuser' is deprecated.")
            print("   Use 'uv run python oppdemo.py superuser' instead.")
            print()
            await run_superuser()
        elif args.command == "users":
            print("⚠️  DEPRECATION WARNING: 'oppman.py users' is deprecated.")
            print("   Use 'uv run python oppdemo.py users' instead.")
            print()
            await run_users()
        elif args.command == "products":
            print("⚠️  DEPRECATION WARNING: 'oppman.py products' is deprecated.")
            print("   Use 'uv run python oppdemo.py products' instead.")
            print()
            await run_products()
        elif args.command == "webinars":
            print("⚠️  DEPRECATION WARNING: 'oppman.py webinars' is deprecated.")
            print("   Use 'uv run python oppdemo.py webinars' instead.")
            print()
            await run_webinars()
        elif args.command == "download_photos":
            print("⚠️  DEPRECATION WARNING: 'oppman.py download_photos' is deprecated.")
            print("   Use 'uv run python oppdemo.py download_photos' instead.")
            print()
            await run_download_photos()
        elif args.command == "registrants":
            print("⚠️  DEPRECATION WARNING: 'oppman.py registrants' is deprecated.")
            print("   Use 'uv run python oppdemo.py registrants' instead.")
            print()
            await run_registrants()
        elif args.command == "clear_registrants":
            print("⚠️  DEPRECATION WARNING: 'oppman.py clear_registrants' is deprecated.")
            print("   Use 'uv run python oppdemo.py clear_registrants' instead.")
            print()
            await run_clear_registrants()
        elif args.command == "check_users":
            print("⚠️  DEPRECATION WARNING: 'oppman.py check_users' is deprecated.")
            print("   Use 'uv run python oppdemo.py check_users' instead.")
            print()
            await run_check_users()
        elif args.command == "test_auth":
            print("⚠️  DEPRECATION WARNING: 'oppman.py test_auth' is deprecated.")
            print("   Use 'uv run python oppdemo.py test_auth' instead.")
            print()
            await test_auth()
        elif args.command == "change_password":
            print("⚠️  DEPRECATION WARNING: 'oppman.py change_password' is deprecated.")
            print("   Use 'uv run python oppdemo.py change_password' instead.")
            print()
            await run_change_password()
        elif args.command == "list_users":
            print("⚠️  DEPRECATION WARNING: 'oppman.py list_users' is deprecated.")
            print("   Use 'uv run python oppdemo.py list_users' instead.")
            print()
            await run_list_users()
    
    # Run the async command
    asyncio.run(run_command())


if __name__ == "__main__":
    main()
