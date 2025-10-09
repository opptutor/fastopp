# db.py - Simple database setup for base_assets
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment (defaults to SQLite for development)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

# Parse the database URL to extract SSL parameters
parsed_url = urlparse(DATABASE_URL)
query_params = parse_qs(parsed_url.query)

# Extract SSL mode from URL parameters
ssl_mode = query_params.get('sslmode', ['prefer'])[0]

# Use the DATABASE_URL as-is (user will specify the driver in environment)
clean_url = DATABASE_URL
if 'sslmode=' in clean_url:
    # Remove sslmode from URL to avoid passing it to the driver
    if '?' in clean_url and 'sslmode=' in clean_url:
        base_url, query_string = clean_url.split('?', 1)
        query_parts = query_string.split('&')
        filtered_parts = [part for part in query_parts if not part.startswith('sslmode=')]
        if filtered_parts:
            clean_url = f"{base_url}?{'&'.join(filtered_parts)}"
        else:
            clean_url = base_url

# Create engine with psycopg3 SSL configuration
connect_args = {}
if parsed_url.scheme.startswith('postgresql'):
    # psycopg3 SSL configuration - more reliable than asyncpg
    if ssl_mode == 'require':
        connect_args['sslmode'] = 'require'
    elif ssl_mode == 'prefer':
        connect_args['sslmode'] = 'prefer'
    elif ssl_mode == 'disable':
        connect_args['sslmode'] = 'disable'
    else:
        # Default to require for cloud providers
        connect_args['sslmode'] = 'require'
    
    # psycopg3 connection settings
    connect_args['connect_timeout'] = 30
    connect_args['application_name'] = 'fastopp'

# Create async engine with conservative settings
async_engine = create_async_engine(
    clean_url,
    echo=True,  # set to False in production
    future=True,
    connect_args=connect_args,
    pool_size=3,  # Reduced pool size for stability
    max_overflow=5,  # Reduced overflow for stability
    pool_timeout=30,  # Conservative timeout
    pool_recycle=1800,  # 30 minutes recycle
    pool_pre_ping=True
)

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# Export async_engine for admin setup
async_engine = async_engine
