from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from urllib.parse import urlparse, parse_qs
from .config import Settings, get_settings


def create_database_engine(settings: Settings = Depends(get_settings)):
    """Create database engine from settings with SSL support"""
    # Parse the database URL to extract SSL parameters
    parsed_url = urlparse(settings.database_url)
    query_params = parse_qs(parsed_url.query)

    # Extract SSL mode from URL parameters
    ssl_mode = query_params.get('sslmode', ['prefer'])[0]

    # Use the DATABASE_URL as-is (user will specify the driver in environment)
    clean_url = settings.database_url
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

    return create_async_engine(
        clean_url,
        echo=settings.environment == "development",
        future=True,
        connect_args=connect_args,
        pool_size=3,  # Reduced pool size for stability
        max_overflow=5,  # Reduced overflow for stability
        pool_timeout=30,  # Conservative timeout
        pool_recycle=1800,  # 30 minutes recycle
        pool_pre_ping=True
    )


def create_session_factory(engine=Depends(create_database_engine)):
    """Create session factory from engine"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )


async def get_db_session(
    session_factory: async_sessionmaker = Depends(create_session_factory)
) -> AsyncSession:
    """Dependency to get database session"""
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
