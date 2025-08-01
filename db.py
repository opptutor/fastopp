# db.py
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment (defaults to SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Database URL formats:
# SQLite (async) - development default
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Alternative formats:
# DATABASE_URL = "sqlite+aiosqlite:///absolute/path/to/test.db"  # Absolute path
# DATABASE_URL = "sqlite+aiosqlite:///:memory:"  # In-memory database
# DATABASE_URL = "sqlite+aiosqlite:///./data/test.db"  # Subdirectory

# PostgreSQL (for production):
# DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

# MySQL (for production):
# DATABASE_URL = "mysql+aiomysql://user:password@localhost/dbname"

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # set to False in production
    future=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# SQLModel will handle the base class
