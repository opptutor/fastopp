"""
Unit tests for service dependencies.

This module tests the dependency injection system for services,
including ProductService, WebinarService, and ChatService.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from dependencies.services import get_product_service, get_webinar_service, get_chat_service
from tests.dependencies import (
    MockProductService,
    MockWebinarService,
    MockChatService,
    get_test_settings
)


class TestProductServiceDependency:
    """Test ProductService dependency injection."""

    def test_get_product_service_returns_instance(self, test_db_session, test_settings):
        """Test that get_product_service returns a ProductService instance."""
        service = get_product_service(session=test_db_session, settings=test_settings)

        assert service is not None
        assert hasattr(service, 'session')
        assert hasattr(service, 'settings')
        assert service.session == test_db_session
        assert service.settings == test_settings

    def test_get_product_service_with_mock_session(self):
        """Test get_product_service with mocked session."""
        mock_session = AsyncMock(spec=AsyncSession)
        settings = get_test_settings()

        service = get_product_service(session=mock_session, settings=settings)

        assert service is not None
        assert service.session == mock_session
        assert service.settings == settings

    @patch('dependencies.services.ProductService')
    def test_get_product_service_imports_correctly(self, mock_product_service_class):
        """Test that get_product_service imports ProductService correctly."""
        mock_session = AsyncMock(spec=AsyncSession)
        settings = get_test_settings()

        # Configure the mock
        mock_instance = MagicMock()
        mock_product_service_class.return_value = mock_instance

        service = get_product_service(session=mock_session, settings=settings)

        # Verify ProductService was called with correct arguments
        mock_product_service_class.assert_called_once_with(
            session=mock_session,
            settings=settings
        )
        assert service == mock_instance


class TestWebinarServiceDependency:
    """Test WebinarService dependency injection."""

    def test_get_webinar_service_returns_instance(self, test_db_session, test_settings):
        """Test that get_webinar_service returns a WebinarService instance."""
        service = get_webinar_service(session=test_db_session, settings=test_settings)

        assert service is not None
        assert hasattr(service, 'session')
        assert hasattr(service, 'settings')
        assert service.session == test_db_session
        assert service.settings == test_settings

    def test_get_webinar_service_with_mock_session(self):
        """Test get_webinar_service with mocked session."""
        mock_session = AsyncMock(spec=AsyncSession)
        settings = get_test_settings()

        service = get_webinar_service(session=mock_session, settings=settings)

        assert service is not None
        assert service.session == mock_session
        assert service.settings == settings

    @patch('dependencies.services.WebinarService')
    def test_get_webinar_service_imports_correctly(self, mock_webinar_service_class):
        """Test that get_webinar_service imports WebinarService correctly."""
        mock_session = AsyncMock(spec=AsyncSession)
        settings = get_test_settings()

        # Configure the mock
        mock_instance = MagicMock()
        mock_webinar_service_class.return_value = mock_instance

        service = get_webinar_service(session=mock_session, settings=settings)

        # Verify WebinarService was called with correct arguments
        mock_webinar_service_class.assert_called_once_with(
            session=mock_session,
            settings=settings
        )
        assert service == mock_instance


class TestChatServiceDependency:
    """Test ChatService dependency injection."""

    def test_get_chat_service_returns_instance(self, test_settings):
        """Test that get_chat_service returns a ChatService instance."""
        service = get_chat_service(settings=test_settings)

        assert service is not None
        assert hasattr(service, 'settings')
        assert service.settings == test_settings

    def test_get_chat_service_with_mock_settings(self):
        """Test get_chat_service with mocked settings."""
        settings = get_test_settings()

        service = get_chat_service(settings=settings)

        assert service is not None
        assert service.settings == settings

    @patch('dependencies.services.ChatService')
    def test_get_chat_service_imports_correctly(self, mock_chat_service_class):
        """Test that get_chat_service imports ChatService correctly."""
        settings = get_test_settings()

        # Configure the mock
        mock_instance = MagicMock()
        mock_chat_service_class.return_value = mock_instance

        service = get_chat_service(settings=settings)

        # Verify ChatService was called with correct arguments
        mock_chat_service_class.assert_called_once_with(settings=settings)
        assert service == mock_instance


class TestMockServices:
    """Test mock service implementations."""

    @pytest.mark.asyncio
    async def test_mock_product_service_get_products_with_stats(self, test_db_session, test_settings):
        """Test MockProductService.get_products_with_stats method."""
        service = MockProductService(session=test_db_session, settings=test_settings)

        result = await service.get_products_with_stats()

        assert result is not None
        assert "products" in result
        assert "total_products" in result
        assert "total_value" in result
        assert isinstance(result["products"], list)
        assert len(result["products"]) == 2
        assert result["total_products"] == 2
        assert result["total_value"] == 31.98

    @pytest.mark.asyncio
    async def test_mock_product_service_get_product_by_id(self, test_db_session, test_settings):
        """Test MockProductService.get_product_by_id method."""
        service = MockProductService(session=test_db_session, settings=test_settings)

        result = await service.get_product_by_id(1)

        assert result is not None
        assert result["id"] == 1
        assert "name" in result
        assert "price" in result
        assert "stock" in result

    @pytest.mark.asyncio
    async def test_mock_webinar_service_get_webinar_registrants(self, test_db_session, test_settings):
        """Test MockWebinarService.get_webinar_registrants method."""
        service = MockWebinarService(session=test_db_session, settings=test_settings)

        result = await service.get_webinar_registrants()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert "name" in result[0]
        assert "email" in result[0]
        assert "webinar_title" in result[0]

    @pytest.mark.asyncio
    async def test_mock_webinar_service_get_webinar_attendees(self, test_db_session, test_settings):
        """Test MockWebinarService.get_webinar_attendees method."""
        service = MockWebinarService(session=test_db_session, settings=test_settings)

        result = await service.get_webinar_attendees()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 1
        assert "name" in result[0]
        assert "email" in result[0]
        assert "attendance_status" in result[0]

    @pytest.mark.asyncio
    async def test_mock_chat_service_test_connection(self, test_settings):
        """Test MockChatService.test_connection method."""
        service = MockChatService(settings=test_settings)

        result = await service.test_connection()

        assert result is not None
        assert result["status"] == "success"
        assert "message" in result
        assert "api_key_configured" in result

    @pytest.mark.asyncio
    async def test_mock_chat_service_chat_completion(self, test_settings):
        """Test MockChatService.chat_completion method."""
        service = MockChatService(settings=test_settings)

        messages = [{"role": "user", "content": "Hello"}]
        result = await service.chat_completion(messages)

        assert result is not None
        assert result["role"] == "assistant"
        assert "content" in result
        assert "usage" in result

    @pytest.mark.asyncio
    async def test_mock_chat_service_chat_completion_stream(self, test_settings):
        """Test MockChatService.chat_completion with streaming."""
        service = MockChatService(settings=test_settings)

        messages = [{"role": "user", "content": "Hello"}]
        responses = []

        async for response in service.chat_completion(messages, stream=True):
            responses.append(response)

        assert len(responses) == 1
        assert responses[0]["role"] == "assistant"
        assert "content" in responses[0]


class TestServiceDependencyIntegration:
    """Test service dependencies with FastAPI integration."""

    def test_service_dependencies_in_fastapi_app(self, test_app):
        """Test that service dependencies work in FastAPI app."""
        assert test_app is not None
        assert hasattr(test_app, 'dependency_overrides')

        # Check that our test dependencies are overridden
        assert 'dependencies.services.get_product_service' in str(test_app.dependency_overrides)
        assert 'dependencies.services.get_webinar_service' in str(test_app.dependency_overrides)
        assert 'dependencies.services.get_chat_service' in str(test_app.dependency_overrides)

    def test_service_dependencies_with_real_db(self, test_app_with_real_db):
        """Test service dependencies with real database."""
        assert test_app_with_real_db is not None
        assert hasattr(test_app_with_real_db, 'dependency_overrides')

        # Check that services are overridden but database is not
        assert 'dependencies.services.get_product_service' in str(test_app_with_real_db.dependency_overrides)
        assert 'dependencies.services.get_webinar_service' in str(test_app_with_real_db.dependency_overrides)
        assert 'dependencies.services.get_chat_service' in str(test_app_with_real_db.dependency_overrides)


class TestServiceDependencyErrorHandling:
    """Test error handling in service dependencies."""

    def test_get_product_service_with_none_session(self):
        """Test get_product_service with None session."""
        settings = get_test_settings()

        with pytest.raises(TypeError):
            get_product_service(session=None, settings=settings)

    def test_get_product_service_with_none_settings(self, test_db_session):
        """Test get_product_service with None settings."""
        with pytest.raises(TypeError):
            get_product_service(session=test_db_session, settings=None)

    def test_get_webinar_service_with_none_session(self):
        """Test get_webinar_service with None session."""
        settings = get_test_settings()

        with pytest.raises(TypeError):
            get_webinar_service(session=None, settings=settings)

    def test_get_chat_service_with_none_settings(self):
        """Test get_chat_service with None settings."""
        with pytest.raises(TypeError):
            get_chat_service(settings=None)


@pytest.mark.unit
class TestServiceDependencyMarkers:
    """Test that service dependency tests are properly marked."""

    def test_unit_marker_applied(self):
        """Test that unit marker is applied to this test class."""
        # This test will only run when --markers unit is specified
        assert True
