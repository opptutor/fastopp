#!/usr/bin/env python3
"""
Database Reset Script
Resets the database without command line access
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.init_db import init_db
from oppman import delete_database, backup_database


async def reset_database():
    """Reset the database completely"""
    print("🔄 Starting database reset...")
    
    # Step 1: Backup current database if it exists
    print("📦 Backing up current database...")
    backup_database()
    
    # Step 2: Delete current database
    print("🗑️  Deleting current database...")
    delete_database()
    
    # Step 3: Initialize fresh database
    print("🔄 Initializing fresh database...")
    await init_db()
    
    print("✅ Database reset complete!")
    print("💡 You can now run 'uv run python oppdemo.py init' to add sample data")


if __name__ == "__main__":
    asyncio.run(reset_database())
