from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from typing import Annotated
from .config import Settings, get_settings


def create_database_engine(settings: Settings) -> AsyncEngine:
    """Create database engine from settings"""
    return create_async_engine(
        settings.database_url,
        echo=settings.environment == "development",
        future=True
    )


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create session factory from engine"""
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False
    )


async def get_db_session(request: Request = None):
    """Dependency to get database session"""
    if request is None:
        # For testing - create a simple session
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.pool import StaticPool
        engine = create_async_engine(
            "sqlite+aiosqlite:///:memory:",
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
            echo=False,
        )
        async with engine.begin() as conn:
            from models import SQLModel
            await conn.run_sync(SQLModel.metadata.create_all)
        
        session = AsyncSession(engine, expire_on_commit=False)
        try:
            yield session
        finally:
            await session.close()
            await engine.dispose()
    else:
        # For production - use app state
        session_factory = request.app.state.session_factory
        async with session_factory() as session:
            try:
                yield session
            finally:
                await session.close()


def get_db_session_dependency():
    """Factory function to create database session dependency"""
    async def _get_db_session(request: Request) -> AsyncSession:
        session_factory = request.app.state.session_factory
        async with session_factory() as session:
            try:
                yield session
            finally:
                await session.close()
    return _get_db_session
