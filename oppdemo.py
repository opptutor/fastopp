#!/usr/bin/env python3
"""
Oppkey Demo Management Tool (oppdemo.py)
A tool for managing demo files, switching between demo and minimal application modes,
and initializing demo data (users, products, webinars, registrants, photos).
"""
import argparse
import asyncio
import filecmp
import os
import shutil
import sys
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
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all script files are in the scripts/ directory")
    sys.exit(1)


def ensure_backup_dir():
    """Ensure backups directory exists and return its path"""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    return backup_dir


def ensure_upload_dirs():
    """Ensure static upload directories exist regardless of current working directory."""
    project_root = Path(__file__).resolve().parent
    uploads_root = project_root / "static" / "uploads"
    photos_dir = uploads_root / "photos"
    sample_photos_dir = uploads_root / "sample_photos"
    uploads_root.mkdir(parents=True, exist_ok=True)
    photos_dir.mkdir(parents=True, exist_ok=True)
    sample_photos_dir.mkdir(parents=True, exist_ok=True)


def create_backup_path(original_file: Path, operation: str) -> Path:
    """Create a backup path in the backups directory"""
    backup_dir = ensure_backup_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create operation-specific subdirectory
    operation_dir = backup_dir / operation
    operation_dir.mkdir(exist_ok=True)
    
    # Create backup filename with timestamp
    backup_filename = f"{original_file.name}.{timestamp}"
    return operation_dir / backup_filename


# Demo Data Initialization Functions
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


def save_demo_files():
    """Save demo files to demo_assets directory"""
    print("🔄 Saving demo files to demo_assets...")
    
    # Ensure demo_assets directory exists
    demo_assets = Path("demo_assets")
    demo_assets.mkdir(exist_ok=True)
    
    # Create subdirectories
    (demo_assets / "templates").mkdir(exist_ok=True)
    (demo_assets / "templates" / "partials").mkdir(exist_ok=True)
    (demo_assets / "static").mkdir(exist_ok=True)
    (demo_assets / "static" / "images").mkdir(exist_ok=True)
    (demo_assets / "static" / "css").mkdir(exist_ok=True)
    (demo_assets / "static" / "js").mkdir(exist_ok=True)
    (demo_assets / "routes").mkdir(exist_ok=True)
    (demo_assets / "services").mkdir(exist_ok=True)
    (demo_assets / "scripts").mkdir(exist_ok=True)
    
    files_copied = 0
    
    try:
        # Backup templates (all root HTML files)
        print("📄 Backing up templates...")
        templates_root = Path("templates")
        if templates_root.exists():
            for src in templates_root.glob("*.html"):
                dst = demo_assets / "templates" / src.name
                shutil.copy2(src, dst)
                print(f"  ✅ templates/{src.name}")
                files_copied += 1
        
        # Backup template partials
        partials_src = Path("templates/partials")
        if partials_src.exists():
            partials_dst = demo_assets / "templates/partials"
            for partial_file in partials_src.glob("*.html"):
                shutil.copy2(partial_file, partials_dst / partial_file.name)
                print(f"  ✅ partials/{partial_file.name}")
                files_copied += 1
        
        # Backup static files
        print("🎨 Backing up static files...")
        
        # Images
        images_src = Path("static/images")
        if images_src.exists():
            images_dst = demo_assets / "static/images"
            for image_file in images_src.glob("*.jpg"):
                shutil.copy2(image_file, images_dst / image_file.name)
                print(f"  ✅ images/{image_file.name}")
                files_copied += 1
        
        # CSS and JS
        for subdir in ["css", "js"]:
            subdir_src = Path(f"static/{subdir}")
            if subdir_src.exists():
                subdir_dst = demo_assets / f"static/{subdir}"
                for file in subdir_src.glob("*"):
                    if file.is_file():
                        shutil.copy2(file, subdir_dst / file.name)
                        print(f"  ✅ {subdir}/{file.name}")
                        files_copied += 1
        
        # Uploads (copy only sample_photos, exclude user uploads)
        uploads_src = Path("static/uploads")
        if uploads_src.exists():
            uploads_dst = demo_assets / "static/uploads"
            uploads_dst.mkdir(parents=True, exist_ok=True)
            
            # Copy only sample_photos directory (exclude photos with user uploads)
            sample_photos_src = uploads_src / "sample_photos"
            if sample_photos_src.exists():
                sample_photos_dst = uploads_dst / "sample_photos"
                if sample_photos_dst.exists():
                    shutil.rmtree(sample_photos_dst)
                shutil.copytree(sample_photos_src, sample_photos_dst)
                print("  ✅ uploads/sample_photos/")
                files_copied += 1
            
            # Create .gitkeep to preserve directory structure
            gitkeep_file = uploads_dst / ".gitkeep"
            if not gitkeep_file.exists():
                gitkeep_file.touch()
                print("  ✅ uploads/.gitkeep")

        # Other static files in root (like LICENSE, favicon.ico, etc.)
        static_root = Path("static")
        if static_root.exists():
            for static_file in static_root.glob("*"):
                if static_file.is_file() and static_file.name not in ["uploads"]:
                    # Skip directories that are handled separately
                    if not static_file.is_dir():
                        shutil.copy2(static_file, demo_assets / "static" / static_file.name)
                        print(f"  ✅ {static_file.name}")
                        files_copied += 1
        
        # Backup routes (all .py files)
        print("🛣️  Backing up routes...")
        routes_src_dir = Path("routes")
        if routes_src_dir.exists():
            for src in routes_src_dir.glob("*.py"):
                dst = demo_assets / "routes" / src.name
                shutil.copy2(src, dst)
                print(f"  ✅ routes/{src.name}")
                files_copied += 1
        
        # Backup services
        print("🔧 Backing up services...")
        service_files = [
            "services/chat_service.py",
            "services/product_service.py",
            "services/webinar_service.py"
        ]
        
        for service_file in service_files:
            src = Path(service_file)
            if src.exists():
                dst = demo_assets / service_file
                shutil.copy2(src, dst)
                print(f"  ✅ {service_file}")
                files_copied += 1
        
        # Backup models
        print("📊 Backing up models...")
        models_src = Path("models.py")
        if models_src.exists():
            shutil.copy2(models_src, demo_assets / "models.py")
            print("  ✅ models.py")
            files_copied += 1
        
        # Backup main.py (application entrypoint)
        print("📄 Backing up main.py...")
        main_src = Path("main.py")
        if main_src.exists():
            shutil.copy2(main_src, demo_assets / "main.py")
            print("  ✅ main.py")
            files_copied += 1
        
        # Backup sample data scripts
        print("📝 Backing up sample data scripts...")
        script_files = [
            "scripts/add_sample_products.py",
            "scripts/add_sample_webinar_registrants.py",
            "scripts/download_sample_photos.py"
        ]
        
        for script_file in script_files:
            src = Path(script_file)
            if src.exists():
                dst = demo_assets / script_file
                shutil.copy2(src, dst)
                print(f"  ✅ {script_file}")
                files_copied += 1
        
        print("\n✅ Demo save completed successfully!")
        print(f"📊 Total files saved: {files_copied}")
        print(f"📁 Save location: {demo_assets.absolute()}")
        print("\n📋 To restore demo files:")
        print("   uv run python oppdemo.py restore")
        print("   # or")
        print("   ./demo_assets/restore_demo.sh")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to save demo files: {e}")
        return False


def restore_demo_files():
    """Restore demo files from demo_assets directory"""
    print("🔄 Restoring demo files from backup...")
    
    demo_assets = Path("demo_assets")
    if not demo_assets.exists():
        print("❌ Error: demo_assets directory not found!")
        print("Please run 'uv run python oppdemo.py save' first to create a save.")
        return False
    
    files_restored = 0
    
    try:
        # Ensure base destination directories exist
        Path("templates").mkdir(parents=True, exist_ok=True)
        Path("templates/partials").mkdir(parents=True, exist_ok=True)
        Path("static").mkdir(parents=True, exist_ok=True)
        Path("static/images").mkdir(parents=True, exist_ok=True)
        Path("static/css").mkdir(parents=True, exist_ok=True)
        Path("static/js").mkdir(parents=True, exist_ok=True)
        Path("routes").mkdir(parents=True, exist_ok=True)
        Path("services").mkdir(parents=True, exist_ok=True)
        Path("scripts").mkdir(parents=True, exist_ok=True)

        # Restore main.py (application entrypoint)
        print("📄 Restoring main.py...")
        main_src = demo_assets / "main.py"
        main_dest = Path("main.py")
        if main_src.exists():
            if main_dest.exists():
                backup_main = create_backup_path(main_dest, "restore")
                shutil.copy2(main_dest, backup_main)
                print(f"  ✅ Backed up current main.py to {backup_main}")
            shutil.copy2(main_src, main_dest)
            print("  ✅ Restored main.py")
            files_restored += 1

        # Restore templates
        print("📄 Restoring templates...")
        templates_src = demo_assets / "templates"
        templates_dest = Path("templates")
        
        if templates_src.exists():
            # Copy individual template files
            for template_file in templates_src.glob("*.html"):
                dest_file = templates_dest / template_file.name
                shutil.copy2(template_file, dest_file)
                print(f"  ✅ Restored {template_file.name}")
                files_restored += 1
            
            # Copy partials directory
            partials_src = templates_src / "partials"
            partials_dest = templates_dest / "partials"
            
            if partials_src.exists():
                if partials_dest.exists():
                    shutil.rmtree(partials_dest)
                shutil.copytree(partials_src, partials_dest)
                print("  ✅ Restored partials/")
        
        # Restore static files
        print("🎨 Restoring static files...")
        static_src = demo_assets / "static"
        static_dest = Path("static")
        
        if static_src.exists():
            # Copy images
            images_src = static_src / "images"
            images_dest = static_dest / "images"
            
            if images_src.exists():
                if images_dest.exists():
                    shutil.rmtree(images_dest)
                shutil.copytree(images_src, images_dest)
                print("  ✅ Restored images/")
            
            # Copy other static files
            for static_file in static_src.glob("*"):
                if static_file.is_file() and static_file.name != "uploads":
                    dest_file = static_dest / static_file.name
                    shutil.copy2(static_file, dest_file)
                    print(f"  ✅ Restored {static_file.name}")
                    files_restored += 1
            
            # Copy CSS and JS directories
            for subdir in ["css", "js"]:
                subdir_src = static_src / subdir
                subdir_dest = static_dest / subdir
                
                if subdir_src.exists():
                    if subdir_dest.exists():
                        shutil.rmtree(subdir_dest)
                    shutil.copytree(subdir_src, subdir_dest)
                    print(f"  ✅ Restored {subdir}/")
            
            # Restore uploads (only sample_photos)
            uploads_src = static_src / "uploads"
            uploads_dest = static_dest / "uploads"
            
            if uploads_src.exists():
                uploads_dest.mkdir(parents=True, exist_ok=True)
                
                # Restore sample_photos directory
                sample_photos_src = uploads_src / "sample_photos"
                if sample_photos_src.exists():
                    sample_photos_dest = uploads_dest / "sample_photos"
                    if sample_photos_dest.exists():
                        shutil.rmtree(sample_photos_dest)
                    shutil.copytree(sample_photos_src, sample_photos_dest)
                    print("  ✅ Restored uploads/sample_photos/")
                
                # Ensure .gitkeep exists
                gitkeep_file = uploads_dest / ".gitkeep"
                if not gitkeep_file.exists():
                    gitkeep_file.touch()
                    print("  ✅ Ensured uploads/.gitkeep")
        
        # Restore routes
        print("🛣️  Restoring routes...")
        routes_src = demo_assets / "routes"
        routes_dest = Path("routes")
        
        if routes_src.exists():
            for route_file in routes_src.glob("*.py"):
                dest_file = routes_dest / route_file.name
                shutil.copy2(route_file, dest_file)
                print(f"  ✅ Restored {route_file.name}")
                files_restored += 1
        
        # Restore services
        print("🔧 Restoring services...")
        services_src = demo_assets / "services"
        services_dest = Path("services")
        
        if services_src.exists():
            for service_file in services_src.glob("*.py"):
                dest_file = services_dest / service_file.name
                shutil.copy2(service_file, dest_file)
                print(f"  ✅ Restored {service_file.name}")
                files_restored += 1
        
        # Restore models
        print("📊 Restoring models...")
        models_src = demo_assets / "models.py"
        models_dest = Path("models.py")
        
        if models_src.exists():
            shutil.copy2(models_src, models_dest)
            print("  ✅ Restored models.py")
            files_restored += 1
        
        # Copy sample data scripts
        print("📝 Restoring sample data scripts...")
        scripts_src = demo_assets / "scripts"
        scripts_dest = Path("scripts")
        
        if scripts_src.exists():
            for script_file in scripts_src.glob("*.py"):
                dest_file = scripts_dest / script_file.name
                shutil.copy2(script_file, dest_file)
                print(f"  ✅ Restored {script_file.name}")
                files_restored += 1

        # Supplement missing required files from original working copy if available
        print("🔍 Checking original working copy for missing files...")
        original_root = Path("../original/fastopp").resolve()
        if original_root.exists():
            # Required templates
            for tpl_name in ["index.html", "login.html"]:
                dst = Path("templates") / tpl_name
                src = original_root / "templates" / tpl_name
                if not dst.exists() and src.exists():
                    shutil.copy2(src, dst)
                    print(f"  ➕ Restored missing template from original: {tpl_name}")
                    files_restored += 1

            # Ensure routes package and required route files
            routes_pkg = Path("routes")
            (routes_pkg).mkdir(parents=True, exist_ok=True)
            init_dst = routes_pkg / "__init__.py"
            if not init_dst.exists():
                # Copy from original if present, else create empty
                init_src = original_root / "routes" / "__init__.py"
                if init_src.exists():
                    shutil.copy2(init_src, init_dst)
                else:
                    init_dst.write_text("")
                print("  ➕ Ensured routes/__init__.py")

            for route_name in ["auth.py", "webinar.py"]:
                dst = routes_pkg / route_name
                src = original_root / "routes" / route_name
                if not dst.exists() and src.exists():
                    shutil.copy2(src, dst)
                    print(f"  ➕ Restored missing route from original: {route_name}")
                    files_restored += 1
        else:
            print("  ℹ️  Original working copy not found at ../original/fastopp (skipping supplement)")
        
        print("\n✅ Demo restoration completed successfully!")
        print(f"📊 Total files restored: {files_restored}")
        print("\n📋 Next steps:")
        print("1. Run sample data scripts to populate the database:")
        print("   uv run python scripts/add_sample_products.py")
        print("   uv run python scripts/add_sample_webinar_registrants.py")
        print("   uv run python scripts/download_sample_photos.py")
        print("2. Start the application: uv run python main.py")
        print("3. Visit the demo pages:")
        print("   - http://localhost:8000/ai-demo")
        print("   - http://localhost:8000/database-demo")
        print("   - http://localhost:8000/design-demo")
        print("   - http://localhost:8000/webinar-demo")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to restore demo files: {e}")
        return False


def destroy_demo_files():
    """Destroy demo files and switch to minimal base application"""
    print("🗑️  Destroying demo files and switching to minimal application...")
    
    try:
        # Step 1: Copy main.py from base_assets to root
        print("📄 Copying minimal main.py from base_assets...")
        base_main = Path("base_assets/main.py")
        if not base_main.exists():
            print("❌ Error: base_assets/main.py not found!")
            print("Please ensure base_assets directory exists with main.py")
            return False
        
        # Backup current main.py if it exists
        current_main = Path("main.py")
        if current_main.exists():
            backup_main = create_backup_path(current_main, "destroy")
            shutil.copy2(current_main, backup_main)
            print(f"  ✅ Backed up current main.py to {backup_main}")
        
        # Copy base main.py to root
        shutil.copy2(base_main, current_main)
        print("  ✅ Copied base_assets/main.py to main.py")
        
        # Step 2: Remove services directory
        print("🔧 Removing services directory...")
        services_dir = Path("services")
        if services_dir.exists():
            shutil.rmtree(services_dir)
            print("  ✅ Removed services/")
        else:
            print("  ℹ️  services/ directory not found")
        
        # Step 3: Delete SQLite database
        print("🗄️  Deleting SQLite database...")
        db_path = Path("test.db")
        if db_path.exists():
            # Backup database first
            backup_db = create_backup_path(db_path, "destroy")
            shutil.copy2(db_path, backup_db)
            print(f"  ✅ Backed up database to {backup_db}")
            
            db_path.unlink()
            print("  ✅ Deleted test.db")
        else:
            print("  ℹ️  test.db not found")
        
        # Step 4: Replace routes directory with base_assets routes
        print("🛣️  Replacing routes directory with base_assets routes...")
        routes_dir = Path("routes")
        base_routes = Path("base_assets/routes")
        
        if routes_dir.exists():
            shutil.rmtree(routes_dir)
            print("  ✅ Removed existing routes/")
        
        if base_routes.exists():
            shutil.copytree(base_routes, routes_dir)
            print("  ✅ Copied base_assets/routes to routes/")
        else:
            print("  ❌ Error: base_assets/routes not found!")
            print("Please ensure base_assets/routes directory exists")
            return False
        
        # Step 5: Remove static directory
        print("🎨 Removing static directory...")
        static_dir = Path("static")
        if static_dir.exists():
            shutil.rmtree(static_dir)
            print("  ✅ Removed static/")
        else:
            print("  ℹ️  static/ directory not found")
        
        # Step 6: Replace templates directory with base_assets templates
        print("📄 Replacing templates directory with base_assets templates...")
        templates_dir = Path("templates")
        base_templates = Path("base_assets/templates")
        
        if templates_dir.exists():
            shutil.rmtree(templates_dir)
            print("  ✅ Removed existing templates/")
        
        if base_templates.exists():
            shutil.copytree(base_templates, templates_dir)
            print("  ✅ Copied base_assets/templates to templates/")
        else:
            print("  ❌ Error: base_assets/templates not found!")
            print("Please ensure base_assets/templates directory exists")
            return False
        
        print("\n✅ Demo destruction completed successfully!")
        print("🔄 Switched to minimal FastAPI application with authentication")
        print("\n📋 Next steps:")
        print("1. Start the minimal application:")
        print("   uv run python main.py")
        print("2. Visit the application:")
        print("   - http://localhost:8000/ (home page with navigation)")
        print("   - http://localhost:8000/login (authentication)")
        print("   - http://localhost:8000/protected (password-protected content)")
        print("   - http://localhost:8000/admin/ (admin panel)")
        print("   - http://localhost:8000/health (health check)")
        print("\n💡 To restore the full demo later:")
        print("   uv run python oppdemo.py restore")
        print("   uv run python oppman.py init")
        print("   uv run python oppman.py runserver")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to destroy demo files: {e}")
        return False


def diff_demo_files():
    """Show differences between current demo files and demo_assets save"""
    print("🔍 Comparing current demo files with demo_assets save...")
    
    demo_assets = Path("demo_assets")
    if not demo_assets.exists():
        print("❌ Error: demo_assets directory not found!")
        print("Please run 'uv run python oppdemo.py save' first to create a save.")
        return False
    
    differences: dict[str, list[str]] = {
        'added': [],
        'modified': [],
        'deleted': [],
        'missing_backup': []
    }
    
    try:
        # Compare templates
        print("📄 Comparing templates...")
        templates_src = Path("templates")
        templates_backup = demo_assets / "templates"
        
        if templates_src.exists() and templates_backup.exists():
            # Compare root template files
            for template_file in templates_src.glob("*.html"):
                backup_file = templates_backup / template_file.name
                if not backup_file.exists():
                    differences['added'].append(f"templates/{template_file.name}")
                else:
                    # Check if files are different
                    if not filecmp.cmp(template_file, backup_file, shallow=False):
                        differences['modified'].append(f"templates/{template_file.name}")
            
            # Check for deleted files
            for backup_file in templates_backup.glob("*.html"):
                src_file = templates_src / backup_file.name
                if not src_file.exists():
                    differences['deleted'].append(f"templates/{backup_file.name}")
            
            # Compare partials
            partials_src = templates_src / "partials"
            partials_backup = templates_backup / "partials"
            
            if partials_src.exists() and partials_backup.exists():
                for partial_file in partials_src.glob("*.html"):
                    backup_file = partials_backup / partial_file.name
                    if not backup_file.exists():
                        differences['added'].append(f"templates/partials/{partial_file.name}")
                    else:
                        if not filecmp.cmp(partial_file, backup_file, shallow=False):
                            differences['modified'].append(f"templates/partials/{partial_file.name}")
                
                for backup_file in partials_backup.glob("*.html"):
                    src_file = partials_src / backup_file.name
                    if not src_file.exists():
                        differences['deleted'].append(f"templates/partials/{backup_file.name}")
        
        # Compare static files
        print("🎨 Comparing static files...")
        static_src = Path("static")
        static_backup = demo_assets / "static"
        
        if static_src.exists() and static_backup.exists():
            # Compare root static files
            for static_file in static_src.glob("*"):
                if static_file.is_file() and static_file.name != "uploads":
                    backup_file = static_backup / static_file.name
                    if not backup_file.exists():
                        differences['added'].append(f"static/{static_file.name}")
                    else:
                        if not filecmp.cmp(static_file, backup_file, shallow=False):
                            differences['modified'].append(f"static/{static_file.name}")
            
            # Check for deleted files
            for backup_file in static_backup.glob("*"):
                if backup_file.is_file() and backup_file.name != "uploads":
                    src_file = static_src / backup_file.name
                    if not src_file.exists():
                        differences['deleted'].append(f"static/{backup_file.name}")
            
            # Compare subdirectories (css, js, images)
            for subdir in ["css", "js", "images"]:
                subdir_src = static_src / subdir
                subdir_backup = static_backup / subdir
                
                if subdir_src.exists() and subdir_backup.exists():
                    for file in subdir_src.glob("*"):
                        if file.is_file():
                            backup_file = subdir_backup / file.name
                            if not backup_file.exists():
                                differences['added'].append(f"static/{subdir}/{file.name}")
                            else:
                                if not filecmp.cmp(file, backup_file, shallow=False):
                                    differences['modified'].append(f"static/{subdir}/{file.name}")
                    
                    for backup_file in subdir_backup.glob("*"):
                        if backup_file.is_file():
                            src_file = subdir_src / backup_file.name
                            if not src_file.exists():
                                differences['deleted'].append(f"static/{subdir}/{backup_file.name}")
            
            # Compare uploads (only sample_photos)
            uploads_src = static_src / "uploads"
            uploads_backup = static_backup / "uploads"
            
            if uploads_src.exists() and uploads_backup.exists():
                sample_photos_src = uploads_src / "sample_photos"
                sample_photos_backup = uploads_backup / "sample_photos"
                
                if sample_photos_src.exists() and sample_photos_backup.exists():
                    for file in sample_photos_src.glob("*"):
                        if file.is_file():
                            backup_file = sample_photos_backup / file.name
                            if not backup_file.exists():
                                differences['added'].append(f"static/uploads/sample_photos/{file.name}")
                            else:
                                if not filecmp.cmp(file, backup_file, shallow=False):
                                    differences['modified'].append(f"static/uploads/sample_photos/{file.name}")
                    
                    for backup_file in sample_photos_backup.glob("*"):
                        if backup_file.is_file():
                            src_file = sample_photos_src / backup_file.name
                            if not src_file.exists():
                                differences['deleted'].append(f"static/uploads/sample_photos/{backup_file.name}")
        
        # Compare routes
        print("🛣️  Comparing routes...")
        routes_src = Path("routes")
        routes_backup = demo_assets / "routes"
        
        if routes_src.exists() and routes_backup.exists():
            for route_file in routes_src.glob("*.py"):
                backup_file = routes_backup / route_file.name
                if not backup_file.exists():
                    differences['added'].append(f"routes/{route_file.name}")
                else:
                    if not filecmp.cmp(route_file, backup_file, shallow=False):
                        differences['modified'].append(f"routes/{route_file.name}")
            
            for backup_file in routes_backup.glob("*.py"):
                src_file = routes_src / backup_file.name
                if not src_file.exists():
                    differences['deleted'].append(f"routes/{backup_file.name}")
        
        # Compare services
        print("🔧 Comparing services...")
        services_src = Path("services")
        services_backup = demo_assets / "services"
        
        if services_src.exists() and services_backup.exists():
            for service_file in services_src.glob("*.py"):
                backup_file = services_backup / service_file.name
                if not backup_file.exists():
                    differences['added'].append(f"services/{service_file.name}")
                else:
                    if not filecmp.cmp(service_file, backup_file, shallow=False):
                        differences['modified'].append(f"services/{service_file.name}")
            
            for backup_file in services_backup.glob("*.py"):
                src_file = services_src / backup_file.name
                if not src_file.exists():
                    differences['deleted'].append(f"services/{backup_file.name}")
        
        # Compare models.py
        print("📊 Comparing models...")
        models_src = Path("models.py")
        models_backup = demo_assets / "models.py"
        
        if models_src.exists() and models_backup.exists():
            if not filecmp.cmp(models_src, models_backup, shallow=False):
                differences['modified'].append("models.py")
        elif models_src.exists() and not models_backup.exists():
            differences['missing_backup'].append("models.py")
        
        # Compare main.py
        print("📄 Comparing main.py...")
        main_src = Path("main.py")
        main_backup = demo_assets / "main.py"
        
        if main_src.exists() and main_backup.exists():
            if not filecmp.cmp(main_src, main_backup, shallow=False):
                differences['modified'].append("main.py")
        elif main_src.exists() and not main_backup.exists():
            differences['missing_backup'].append("main.py")
        
        # Display results
        print("\n📋 Demo Files Comparison Results:")
        print("=" * 50)
        
        if any(differences.values()):
            if differences['added']:
                print(f"\n🟢 Added files ({len(differences['added'])}):")
                for file in sorted(differences['added']):
                    print(f"  + {file}")
            
            if differences['modified']:
                print(f"\n🟡 Modified files ({len(differences['modified'])}):")
                for file in sorted(differences['modified']):
                    print(f"  ~ {file}")
            
            if differences['deleted']:
                print(f"\n🔴 Deleted files ({len(differences['deleted'])}):")
                for file in sorted(differences['deleted']):
                    print(f"  - {file}")
            
            if differences['missing_backup']:
                print(f"\n⚠️  Files missing from backup ({len(differences['missing_backup'])}):")
                for file in sorted(differences['missing_backup']):
                    print(f"  ? {file}")
            
            total_changes = sum(len(diff) for diff in differences.values())
            print(f"\n📊 Summary: {total_changes} total changes detected")
            
            if differences['added'] or differences['modified']:
                print("\n💡 To update save with current changes:")
                print("   uv run python oppdemo.py save")
            
            if differences['deleted']:
                print("\n⚠️  Note: Deleted files will remain in save unless manually removed")
        else:
            print("✅ No differences found! Current demo files match the save.")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to compare demo files: {e}")
        return False


def list_backups():
    """List all available backups"""
    backup_dir = Path("backups")
    if not backup_dir.exists():
        print("ℹ️  No backups directory found")
        return
    
    print("📁 Available Backups:")
    print("=" * 50)
    
    for operation_dir in backup_dir.iterdir():
        if operation_dir.is_dir():
            print(f"\n🔧 {operation_dir.name.upper()} Backups:")
            backups = list(operation_dir.glob("*"))
            if backups:
                for backup in sorted(backups, reverse=True):
                    # Extract timestamp from filename
                    filename = backup.name
                    if "." in filename:
                        base_name = filename.rsplit(".", 1)[0]
                        timestamp = filename.rsplit(".", 1)[1]
                        print(f"  📄 {base_name} - {timestamp}")
                    else:
                        print(f"  📄 {filename}")
            else:
                print("  ℹ️  No backups found")
    
    print(f"\n📁 Backup location: {backup_dir.absolute()}")


def show_help():
    """Show detailed help information"""
    help_text = """
Oppkey Demo Management Tool (oppdemo.py)

A tool for managing demo files, switching between demo and minimal application modes,
and initializing demo data (users, products, webinars, registrants, photos).

USAGE:
    uv run python oppdemo.py <command> [options]

COMMANDS:
    # Demo file management
    save        Save demo files to demo_assets directory
    restore     Restore demo files from demo_assets directory
    destroy     Destroy demo files and switch to minimal application
    diff        Show differences between current demo and save
    backups     List all available backups
    
    # Demo data initialization (moved from oppman.py)
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
    
    help        Show this help message

EXAMPLES:
    # Demo file management
    uv run python oppdemo.py save      # Save demo files
    uv run python oppdemo.py restore   # Restore demo files
    uv run python oppdemo.py destroy   # Switch to minimal app
    uv run python oppdemo.py diff      # Show differences
    uv run python oppdemo.py backups   # List all backups
    
    # Demo data initialization
    uv run python oppdemo.py init      # Full initialization
    uv run python oppdemo.py db        # Initialize database only
    uv run python oppdemo.py users     # Add test users
    uv run python oppdemo.py products  # Add sample products
    uv run python oppdemo.py webinars  # Add sample webinars
    uv run python oppdemo.py download_photos  # Download sample photos
    uv run python oppdemo.py registrants     # Add sample registrants
    uv run python oppdemo.py clear_registrants  # Clear and add fresh registrants
    uv run python oppdemo.py check_users      # Check existing users
    uv run python oppdemo.py test_auth        # Test authentication
    uv run python oppdemo.py change_password  # Change user password
    uv run python oppdemo.py list_users      # List all users

DESCRIPTION:
    This tool helps manage the demo application state and data:
    
    DEMO FILE MANAGEMENT:
    - save: Creates a backup of all demo-related files in demo_assets/
    - restore: Restores the full demo application from backup
    - destroy: Switches to minimal FastAPI application with authentication
    - diff: Shows what files have changed since the last save
    - backups: Lists all available backups organized by operation type
    
    DEMO DATA INITIALIZATION:
    - init: Complete setup with all sample data
    - Individual commands for specific data types
    - User management and authentication testing
    - Sample products, webinars, and registrants
    
    BACKUP SYSTEM:
    All backups are automatically stored in the backups/ directory:
    - backups/destroy/ - Files backed up before switching to minimal mode
    - backups/restore/ - Files backed up before restoring demo mode
    
    The minimal application includes:
    - Basic authentication system
    - Admin panel
    - Health check endpoint
    - Simple home page
    
    The full demo includes:
    - AI chat demo
    - Dashboard demo
    - Design demo
    - Webinar management
    - Product management
    - Sample data and photos
    
    DEFAULT CREDENTIALS:
    Superuser: admin@example.com / admin123
    Test Users: test123 (for all test users)
    """
    print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Oppkey Demo Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Demo file management
  uv run python oppdemo.py save      # Save demo files
  uv run python oppdemo.py restore   # Restore demo files
  uv run python oppdemo.py destroy   # Switch to minimal app
  uv run python oppdemo.py diff      # Show differences
  uv run python oppdemo.py backups   # List all backups
  
  # Demo data initialization
  uv run python oppdemo.py init      # Full initialization
  uv run python oppdemo.py users     # Add test users
  uv run python oppdemo.py products  # Add sample products
        """
    )
    
    parser.add_argument(
        "command",
        nargs="?",
        choices=[
            # Demo file management
            "save", "restore", "destroy", "diff", "backups",
            # Demo data initialization (moved from oppman.py)
            "init", "db", "superuser", "users", "products", "webinars",
            "download_photos", "registrants", "clear_registrants", "check_users",
            "test_auth", "change_password", "list_users",
            "help"
        ],
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
    
    # Handle demo file management commands
    if args.command == "save":
        save_demo_files()
    elif args.command == "restore":
        restore_demo_files()
    elif args.command == "destroy":
        destroy_demo_files()
    elif args.command == "diff":
        diff_demo_files()
    elif args.command == "backups":
        list_backups()
    
    # Handle demo data initialization commands (moved from oppman.py)
    elif args.command in ["init", "db", "superuser", "users", "products", "webinars",
                          "download_photos", "registrants", "clear_registrants", "check_users",
                          "test_auth", "change_password", "list_users"]:
        # Run async commands
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
            elif args.command == "change_password":
                await run_change_password()
            elif args.command == "list_users":
                await run_list_users()
        
        # Run the async command
        asyncio.run(run_command())
    
    else:
        print("❌ Invalid command")
        show_help()


if __name__ == "__main__":
    main()
