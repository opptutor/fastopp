"""
Shared pytest configuration and fixtures for FastOpp testing.

This module provides common fixtures and configuration that can be used
across all test modules in the FastOpp project.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path

from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

from tests.dependencies import (
    get_test_settings,
    get_test_db_session,
    create_test_app,
    create_test_app_with_real_db,
    MockProductService,
    MockWebinarService,
    MockChatService
)


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom settings."""
    # Add custom markers
    config.addinivalue_line("markers", "unit: Unit tests for individual components")
    config.addinivalue_line("markers", "integration: Integration tests for API endpoints")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "auth: Authentication related tests")
    config.addinivalue_line("markers", "database: Database related tests")
    config.addinivalue_line("markers", "services: Service layer tests")
    config.addinivalue_line("markers", "routes: Route handler tests")
    config.addinivalue_line("markers", "performance: Performance and load tests")
    config.addinivalue_line("markers", "state: State management tests (oppdemo.py)")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)
        elif "state" in str(item.fspath):
            item.add_marker(pytest.mark.state)

        # Add slow marker for tests that take longer than 1 second
        if "slow" in item.name or "load" in item.name:
            item.add_marker(pytest.mark.slow)


# Event loop fixtures
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Settings fixtures
@pytest.fixture
def test_settings():
    """Basic test settings fixture."""
    return get_test_settings()


@pytest.fixture
def test_settings_production():
    """Production-like test settings fixture."""
    return get_test_settings(
        environment="production",
        secret_key="production_test_key",
        database_url="sqlite+aiosqlite:///./test_production.db"
    )


@pytest.fixture
def test_settings_development():
    """Development test settings fixture."""
    return get_test_settings(
        environment="development",
        secret_key="dev_test_key",
        database_url="sqlite+aiosqlite:///./test_dev.db"
    )


# Database fixtures
@pytest.fixture
async def test_db_session():
    """Test database session fixture."""
    async for session in get_test_db_session():
        yield session


@pytest.fixture
async def test_db_engine():
    """Test database engine fixture."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
        echo=False,
    )

    # Create tables
    from models import SQLModel
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


# Application fixtures
@pytest.fixture
def test_app():
    """Test FastAPI application with mocked dependencies."""
    return create_test_app()


@pytest.fixture
def test_app_with_real_db():
    """Test FastAPI application with real database but mocked services."""
    return create_test_app_with_real_db()


@pytest.fixture
def test_app_production():
    """Test FastAPI application with production-like settings."""
    production_settings = get_test_settings(
        environment="production",
        secret_key="production_test_key"
    )
    return create_test_app(test_settings=production_settings)


# Client fixtures
@pytest.fixture
def test_client(test_app):
    """Synchronous test client fixture."""
    return TestClient(test_app)


@pytest.fixture
async def async_test_client(test_app):
    """Asynchronous test client fixture."""
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        yield client


# Service mock fixtures
@pytest.fixture
def mock_product_service(test_db_session, test_settings):
    """Mock ProductService fixture."""
    return MockProductService(session=test_db_session, settings=test_settings)


@pytest.fixture
def mock_webinar_service(test_db_session, test_settings):
    """Mock WebinarService fixture."""
    return MockWebinarService(session=test_db_session, settings=test_settings)


@pytest.fixture
def mock_chat_service(test_settings):
    """Mock ChatService fixture."""
    return MockChatService(settings=test_settings)


# Database data fixtures
@pytest.fixture
async def sample_products(test_db_session):
    """Sample products data fixture."""
    from models import Product

    products = [
        Product(name="Test Product 1", price=10.99, stock=100),
        Product(name="Test Product 2", price=20.99, stock=50),
        Product(name="Test Product 3", price=30.99, stock=25),
    ]

    for product in products:
        test_db_session.add(product)

    await test_db_session.commit()
    return products


@pytest.fixture
async def sample_users(test_db_session):
    """Sample users data fixture."""
    from models import User
    import uuid

    users = [
        User(
            id=uuid.uuid4(),
            email="test1@example.com",
            hashed_password="hashed_password_1",
            is_active=True,
            is_staff=False,
            is_superuser=False
        ),
        User(
            id=uuid.uuid4(),
            email="admin@example.com",
            hashed_password="hashed_password_admin",
            is_active=True,
            is_staff=True,
            is_superuser=True
        ),
    ]

    for user in users:
        test_db_session.add(user)

    await test_db_session.commit()
    return users


@pytest.fixture
async def sample_webinar_registrants(test_db_session):
    """Sample webinar registrants data fixture."""
    from models import WebinarRegistrant
    import uuid

    registrants = [
        WebinarRegistrant(
            id=uuid.uuid4(),
            name="John Doe",
            email="john@example.com",
            webinar_title="Test Webinar 1",
            registration_date="2024-01-01T00:00:00"
        ),
        WebinarRegistrant(
            id=uuid.uuid4(),
            name="Jane Smith",
            email="jane@example.com",
            webinar_title="Test Webinar 2",
            registration_date="2024-01-02T00:00:00"
        ),
    ]

    for registrant in registrants:
        test_db_session.add(registrant)

    await test_db_session.commit()
    return registrants


# Temporary directory fixtures
@pytest.fixture
def temp_upload_dir():
    """Temporary upload directory fixture."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def temp_test_dir():
    """Temporary test directory fixture."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


# Authentication fixtures
@pytest.fixture
def test_jwt_token(test_settings):
    """Test JWT token fixture."""
    import jwt
    from datetime import datetime, timedelta

    payload = {
        "sub": "test-user-id",
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }

    return jwt.encode(payload, test_settings.secret_key, algorithm="HS256")


@pytest.fixture
def auth_headers(test_jwt_token):
    """Authentication headers fixture."""
    return {"Authorization": f"Bearer {test_jwt_token}"}


# Performance testing fixtures
@pytest.fixture
def performance_timer():
    """Performance timer fixture for benchmarking."""
    import time

    class PerformanceTimer:
        def __init__(self):
            self.start_time = None
            self.end_time = None

        def start(self):
            self.start_time = time.time()

        def stop(self):
            self.end_time = time.time()
            return self.elapsed

        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None

    return PerformanceTimer()


# State management fixtures
@pytest.fixture
def mock_oppdemo_state():
    """Mock oppdemo.py state for testing."""
    return {
        "current_state": "demo",
        "base_assets_exists": True,
        "demo_assets_exists": True,
        "services_exists": True
    }


# Error simulation fixtures
@pytest.fixture
def mock_database_error():
    """Mock database error for testing error handling."""
    from sqlalchemy.exc import SQLAlchemyError
    return SQLAlchemyError("Mock database error")


@pytest.fixture
def mock_http_error():
    """Mock HTTP error for testing error handling."""
    from fastapi import HTTPException
    return HTTPException(status_code=500, detail="Mock HTTP error")


# Cleanup fixtures
@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Cleanup test files after each test."""
    yield
    # Cleanup any test files that might have been created
    import glob
    import os

    test_files = glob.glob("test_*.db")
    for file in test_files:
        try:
            os.remove(file)
        except OSError:
            pass


# Test data validation fixtures
@pytest.fixture
def validate_json_response():
    """Fixture for validating JSON response structure."""
    def _validate(response_data, expected_keys=None, expected_types=None):
        """Validate JSON response data structure."""
        if expected_keys:
            for key in expected_keys:
                assert key in response_data, f"Missing expected key: {key}"

        if expected_types:
            for key, expected_type in expected_types.items():
                if key in response_data:
                    assert isinstance(response_data[key], expected_type), \
                        f"Key '{key}' should be {expected_type}, got {type(response_data[key])}"

    return _validate


# Async test utilities
@pytest.fixture
def async_test_runner():
    """Fixture for running async test functions."""
    def _run_async(async_func, *args, **kwargs):
        """Run an async function in the event loop."""
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(async_func(*args, **kwargs))

    return _run_async
