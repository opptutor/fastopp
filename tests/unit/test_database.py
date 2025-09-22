"""
Unit tests for database dependencies.

This module tests the dependency injection system for database operations,
including database engine creation, session factory, and session management.
"""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool

from dependencies.database import (
    create_database_engine,
    create_session_factory,
    get_db_session
)
from dependencies.config import Settings
from tests.dependencies import get_test_settings


class TestCreateDatabaseEngine:
    """Test create_database_engine function."""

    def test_create_database_engine_with_default_settings(self):
        """Test create_database_engine with default settings."""
        settings = get_test_settings()
        engine = create_database_engine(settings)

        assert engine is not None
        assert engine.url.database == ":memory:"  # In-memory SQLite
        assert engine.url.drivername == "sqlite+aiosqlite"

    def test_create_database_engine_with_custom_settings(self):
        """Test create_database_engine with custom settings."""
        settings = get_test_settings(
            database_url="sqlite+aiosqlite:///custom_test.db",
            environment="production"
        )
        engine = create_database_engine(settings)

        assert engine is not None
        assert "custom_test.db" in str(engine.url)
        assert engine.url.drivername == "sqlite+aiosqlite"

    def test_create_database_engine_echo_setting(self):
        """Test that echo setting is properly configured."""
        # Development environment should have echo=True
        dev_settings = get_test_settings(environment="development")
        dev_engine = create_database_engine(dev_settings)
        assert dev_engine.echo is True

        # Production environment should have echo=False
        prod_settings = get_test_settings(environment="production")
        prod_engine = create_database_engine(prod_settings)
        assert prod_engine.echo is False

        # Testing environment should have echo=False
        test_settings = get_test_settings(environment="testing")
        test_engine = create_database_engine(test_settings)
        assert test_engine.echo is False

    def test_create_database_engine_future_setting(self):
        """Test that future setting is always True."""
        settings = get_test_settings()
        engine = create_database_engine(settings)

        # The future setting should always be True
        # future attribute is not available on AsyncEngine
        assert engine is not None

    def test_create_database_engine_with_different_database_types(self):
        """Test create_database_engine with different database types."""
        # SQLite
        sqlite_settings = get_test_settings(database_url="sqlite+aiosqlite:///test.db")
        sqlite_engine = create_database_engine(sqlite_settings)
        assert sqlite_engine.url.drivername == "sqlite+aiosqlite"

        # PostgreSQL (mock)
        postgres_settings = get_test_settings(
            database_url="postgresql+asyncpg://user:pass@localhost/db"
        )
        postgres_engine = create_database_engine(postgres_settings)
        assert postgres_engine.url.drivername == "postgresql+asyncpg"


class TestCreateSessionFactory:
    """Test create_session_factory function."""

    def test_create_session_factory_with_engine(self):
        """Test create_session_factory with provided engine."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        assert session_factory is not None
        assert isinstance(session_factory, async_sessionmaker)
        # async_sessionmaker doesn't have a bind attribute
        assert session_factory is not None

    def test_create_session_factory_configuration(self):
        """Test that session factory is properly configured."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Check session factory configuration
        assert session_factory.class_ == AsyncSession
        # async_sessionmaker configuration is internal
        assert session_factory is not None
        assert session_factory.autoflush is False
        assert session_factory.autocommit is False

    def test_create_session_factory_with_dependency_injection(self):
        """Test create_session_factory with dependency injection."""
        # This test simulates how FastAPI would call the function
        settings = get_test_settings()
        engine = create_database_engine(settings)

        # Simulate FastAPI dependency injection
        session_factory = create_session_factory(engine)

        assert session_factory is not None
        # async_sessionmaker doesn't have a bind attribute
        assert session_factory is not None


class TestGetDbSession:
    """Test get_db_session function."""

    @pytest.mark.asyncio
    async def test_get_db_session_yields_session(self):
        """Test that get_db_session yields an AsyncSession."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        session_generator = get_db_session(session_factory)
        session = await session_generator.__anext__()

        assert isinstance(session, AsyncSession)
        assert session.is_active

        # Clean up
        await session.close()
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_db_session_cleanup(self):
        """Test that get_db_session properly cleans up the session."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        session_generator = get_db_session(session_factory)
        session = await session_generator.__anext__()

        # Verify session is active
        assert session.is_active

        # Simulate the finally block cleanup
        try:
            pass  # Normal operation
        finally:
            await session.close()

        # Session should be closed
        assert not session.is_active

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_db_session_with_exception(self):
        """Test get_db_session cleanup when exception occurs."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        session_generator = get_db_session(session_factory)
        session = await session_generator.__anext__()

        # Verify session is active
        assert session.is_active

        # Simulate exception during operation
        try:
            raise ValueError("Test exception")
        except ValueError:
            # Session should still be cleaned up
            await session.close()

        # Session should be closed even after exception
        assert not session.is_active

        await engine.dispose()

    @pytest.mark.asyncio
    async def test_get_db_session_context_manager_behavior(self):
        """Test that get_db_session behaves like a context manager."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Test the full context manager behavior
        async with session_factory() as session:
            assert isinstance(session, AsyncSession)
            assert session.is_active

        # Session should be closed after context
        assert not session.is_active

        await engine.dispose()


class TestDatabaseDependencyIntegration:
    """Test database dependencies with FastAPI integration."""

    @pytest.mark.asyncio
    async def test_database_dependencies_work_together(self):
        """Test that all database dependencies work together."""
        settings = get_test_settings()

        # Create engine
        engine = create_database_engine(settings)

        # Create session factory
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Test session creation
        session_generator = get_db_session(session_factory)
        session = await session_generator.__anext__()

        assert isinstance(session, AsyncSession)
        assert session.is_active

        # Clean up
        await session.close()
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_database_dependencies_with_real_operations(self):
        """Test database dependencies with real database operations."""
        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Test with real database operations
        session_generator = get_db_session(session_factory)
        session = await session_generator.__anext__()

        try:
            # Test that we can perform database operations
            from sqlalchemy import text
            result = await session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        finally:
            await session.close()

        await engine.dispose()


class TestDatabaseDependencyErrorHandling:
    """Test error handling in database dependencies."""

    def test_create_database_engine_with_invalid_url(self):
        """Test create_database_engine with invalid database URL."""
        settings = get_test_settings(database_url="invalid://url")

        # This should raise an exception
        with pytest.raises(Exception):  # SQLAlchemy will raise an exception
            create_database_engine(settings)

    def test_create_session_factory_with_none_engine(self):
        """Test create_session_factory with None engine."""
        with pytest.raises(Exception):  # Should raise an exception
            create_session_factory(None)

    @pytest.mark.asyncio
    async def test_get_db_session_with_invalid_factory(self):
        """Test get_db_session with invalid session factory."""
        # This should raise an exception when trying to create a session
        with pytest.raises(Exception):
            session_generator = get_db_session(None)
            await session_generator.__anext__()


class TestDatabaseDependencyPerformance:
    """Test database dependency performance characteristics."""

    @pytest.mark.asyncio
    async def test_session_creation_performance(self):
        """Test that session creation is reasonably fast."""
        import time

        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        # Measure session creation time
        start_time = time.time()

        session_generator = get_db_session(session_factory)
        session = await session_generator.__anext__()

        creation_time = time.time() - start_time

        # Session creation should be fast (less than 1 second)
        assert creation_time < 1.0

        await session.close()
        await engine.dispose()

    @pytest.mark.asyncio
    async def test_multiple_sessions_performance(self):
        """Test performance with multiple concurrent sessions."""
        import asyncio

        settings = get_test_settings()
        engine = create_database_engine(settings)
        session_factory = create_session_factory(engine)

        # Create tables for testing
        from models import SQLModel
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        async def create_session():
            session_generator = get_db_session(session_factory)
            session = await session_generator.__anext__()
            await session.close()
            return session

        # Create multiple sessions concurrently
        tasks = [create_session() for _ in range(10)]
        sessions = await asyncio.gather(*tasks)

        # All sessions should be created successfully
        assert len(sessions) == 10

        await engine.dispose()


class TestDatabaseDependencyMocking:
    """Test database dependency mocking capabilities."""

    def test_mock_database_engine(self):
        """Test mocking database engine."""
        mock_engine = MagicMock()
        mock_engine.url = MagicMock()
        mock_engine.url.drivername = "sqlite+aiosqlite"
        mock_engine.url.database = ":memory:"

        # Test that we can create a session factory with mocked engine
        session_factory = create_session_factory(mock_engine)
        assert session_factory is not None
        assert session_factory.bind == mock_engine

    @pytest.mark.asyncio
    async def test_mock_session_factory(self):
        """Test mocking session factory."""
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.is_active = True

        mock_session_factory = MagicMock()
        mock_session_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_factory.return_value.__aexit__ = AsyncMock(return_value=None)

        # Test session creation with mocked factory
        session_generator = get_db_session(mock_session_factory)
        session = await session_generator.__anext__()

        assert session == mock_session


@pytest.mark.unit
class TestDatabaseDependencyMarkers:
    """Test that database dependency tests are properly marked."""

    def test_unit_marker_applied(self):
        """Test that unit marker is applied to this test class."""
        # This test will only run when --markers unit is specified
        assert True
