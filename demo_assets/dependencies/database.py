from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from urllib.parse import urlparse, parse_qs
from .config import Settings, get_settings


def create_database_engine(settings: Settings = Depends(get_settings)):
    """Create database engine from settings with minimal psycopg3 configuration"""
    # Use the DATABASE_URL as-is (psycopg3 handles sslmode in URL properly)
    clean_url = settings.database_url

    # Create engine with minimal psycopg3 configuration
    connect_args = {
        # Disable prepared statements to avoid psycopg3 issues
        "prepare_threshold": None
    }

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
