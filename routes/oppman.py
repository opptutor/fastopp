"""
Oppman API routes for admin management functions
Provides web interface for oppman.py functionality
"""
import asyncio
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from fastapi_users.password import PasswordHelper

from dependencies.auth import get_current_superuser
from models import User
from db import AsyncSessionLocal

router = APIRouter()
templates = Jinja2Templates(directory="templates")


async def change_user_password(email: str, new_password: str) -> dict:
    """Change a user's password by email address"""
    async with AsyncSessionLocal() as session:
        try:
            # Find the user by email
            result = await session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar_one_or_none()
            
            if not user:
                return {"success": False, "message": f"User not found: {email}"}
            
            if not user.is_active:
                return {"success": False, "message": f"User is inactive: {email}"}
            
            # Hash the new password
            password_helper = PasswordHelper()
            hashed_password = password_helper.hash(new_password)
            
            # Update the user's password
            user.hashed_password = hashed_password
            await session.commit()
            
            return {"success": True, "message": f"Password changed successfully for user: {email}"}
            
        except Exception as e:
            await session.rollback()
            return {"success": False, "message": f"Error changing password: {str(e)}"}


async def list_all_users() -> List[dict]:
    """List all users for the admin interface"""
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(User))
            users = result.scalars().all()
            
            user_list = []
            for user in users:
                user_list.append({
                    "id": user.id,
                    "email": user.email,
                    "is_active": user.is_active,
                    "is_superuser": user.is_superuser,
                    "is_staff": user.is_staff,
                    "group": user.group
                })
            
            return user_list
            
        except Exception as e:
            return []


def run_oppman_command(command: str, args: List[str] = None) -> dict:
    """Run oppman command and return result"""
    try:
        cmd = ["uv", "run", "python", "oppman.py", command]
        if args:
            cmd.extend(args)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "success": False,
            "stdout": "",
            "stderr": str(e),
            "command": f"uv run python oppman.py {command}"
        }


@router.get("/", response_class=HTMLResponse)
async def oppman_dashboard(request: Request, current_user: User = Depends(get_current_superuser)):
    """Main oppman admin dashboard"""
    users = await list_all_users()
    return templates.TemplateResponse("oppman.html", {
        "request": request,
        "users": users,
        "current_user": current_user
    })


@router.post("/change-password")
async def change_password_api(
    request: Request,
    email: str = Form(...),
    new_password: str = Form(...),
    current_user: User = Depends(get_current_superuser)
):
    """API endpoint to change user password"""
    if len(new_password) < 6:
        return JSONResponse({
            "success": False,
            "message": "Password must be at least 6 characters long"
        })
    
    result = await change_user_password(email, new_password)
    
    # Check if this is an HTMX request
    if 'hx-request' in request.headers:
        if result["success"]:
            return HTMLResponse(
                f'<div class="alert alert-success" role="alert">✅ {result["message"]}</div>'
            )
        else:
            return HTMLResponse(
                f'<div class="alert alert-error" role="alert">❌ {result["message"]}</div>'
            )
    else:
        return JSONResponse(result)


@router.get("/users")
async def get_users_api(current_user: User = Depends(get_current_superuser)):
    """API endpoint to get all users"""
    users = await list_all_users()
    return JSONResponse({"users": users})


@router.post("/migrate")
async def run_migration(
    request: Request,
    command: str = Form(...),
    message: str = Form(""),
    revision: str = Form(""),
    current_user: User = Depends(get_current_superuser)
):
    """API endpoint to run migration commands"""
    args = []
    
    if command == "create" and message:
        args.append(message)
    elif command in ["upgrade", "downgrade", "show", "stamp"] and revision:
        args.append(revision)
    
    result = run_oppman_command("migrate", [command] + args)
    
    # Check if this is an HTMX request
    if 'hx-request' in request.headers:
        if result["success"]:
            return HTMLResponse(
                f'<div class="alert alert-success" role="alert">✅ Migration {command} completed successfully</div>'
                f'<pre class="mt-2 p-2 bg-base-200 rounded"><code>{result["stdout"]}</code></pre>'
            )
        else:
            return HTMLResponse(
                f'<div class="alert alert-error" role="alert">❌ Migration {command} failed</div>'
                f'<pre class="mt-2 p-2 bg-base-200 rounded"><code>{result["stderr"]}</code></pre>'
            )
    else:
        return JSONResponse(result)


@router.post("/database")
async def run_database_command(
    request: Request,
    command: str = Form(...),
    current_user: User = Depends(get_current_superuser)
):
    """API endpoint to run database commands"""
    if command not in ["backup", "delete", "db"]:
        return JSONResponse({
            "success": False,
            "message": "Invalid database command"
        })
    
    result = run_oppman_command(command)
    
    # Check if this is an HTMX request
    if 'hx-request' in request.headers:
        if result["success"]:
            return HTMLResponse(
                f'<div class="alert alert-success" role="alert">✅ Database {command} completed successfully</div>'
                f'<pre class="mt-2 p-2 bg-base-200 rounded"><code>{result["stdout"]}</code></pre>'
            )
        else:
            return HTMLResponse(
                f'<div class="alert alert-error" role="alert">❌ Database {command} failed</div>'
                f'<pre class="mt-2 p-2 bg-base-200 rounded"><code>{result["stderr"]}</code></pre>'
            )
    else:
        return JSONResponse(result)


@router.post("/user-management")
async def run_user_management_command(
    request: Request,
    command: str = Form(...),
    current_user: User = Depends(get_current_superuser)
):
    """API endpoint to run user management commands"""
    if command not in ["superuser", "check_users", "test_auth", "list_users"]:
        return JSONResponse({
            "success": False,
            "message": "Invalid user management command"
        })
    
    result = run_oppman_command(command)
    
    # Check if this is an HTMX request
    if 'hx-request' in request.headers:
        if result["success"]:
            return HTMLResponse(
                f'<div class="alert alert-success" role="alert">✅ User management {command} completed successfully</div>'
                f'<pre class="mt-2 p-2 bg-base-200 rounded"><code>{result["stdout"]}</code></pre>'
            )
        else:
            return HTMLResponse(
                f'<div class="alert alert-error" role="alert">❌ User management {command} failed</div>'
                f'<pre class="mt-2 p-2 bg-base-200 rounded"><code>{result["stderr"]}</code></pre>'
            )
    else:
        return JSONResponse(result)

