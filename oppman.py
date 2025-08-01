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


async def run_full_init():
    """Run complete initialization: init + superuser + users + products"""
    print("🚀 Running full initialization...")
    
    await run_init()
    await run_superuser()
    await run_users()
    await run_products()
    
    print("✅ Full initialization complete!")
    print("\n📋 Summary:")
    print("- Database initialized")
    print("- Superuser created: admin@example.com / admin123")
    print("- Test users added (password: test123)")
    print("- Sample products added")
    print("\n🌐 Ready to start the application with: uv run uvicorn main:app --reload")


def show_help():
    """Show detailed help information"""
    help_text = """
Oppkey Management Tool (oppman.py)

A comprehensive tool for managing the FastAPI admin application.

USAGE:
    python oppman.py <command> [options]

COMMANDS:
    init        Complete initialization (database + superuser + users + products)
    db          Initialize database only
    superuser   Create superuser only
    users       Add test users only
    products    Add sample products only
    runserver   Start development server with uvicorn --reload
    stopserver  Stop development server
    delete      Delete current database (with backup)
    backup      Backup current database
    help        Show this help message

EXAMPLES:
    # Full initialization (recommended for first-time setup)
    python oppman.py init
    
    # Individual operations
    python oppman.py db
    python oppman.py superuser
    python oppman.py users
    python oppman.py products
    
    # Start development server
    python oppman.py runserver
    
    # Stop development server
    python oppman.py stopserver
    
    # Database management
    python oppman.py backup
    python oppman.py delete

DEFAULT CREDENTIALS:
    Superuser: admin@example.com / admin123
    Test Users: test123 (for all test users)
    
    Test Users Created:
    - john@example.com (active, regular user)
    - jane@example.com (active, regular user)
    - bob@example.com (inactive, regular user)
    - admin2@example.com (active, superuser)

DATABASE:
    - Development: SQLite (test.db)
    - Backup format: test.db.YYYYMMDD_HHMMSS

SERVER:
    - Development server: http://localhost:8000
    - Admin panel: http://localhost:8000/admin/
    - API docs: http://localhost:8000/docs
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
        choices=["init", "db", "superuser", "users", "products", "runserver", "stopserver", "delete", "backup", "help"],
        help="Command to execute"
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
    
    # Run the async command
    asyncio.run(run_command())


if __name__ == "__main__":
    main() 