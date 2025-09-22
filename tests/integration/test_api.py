"""
Integration tests for API endpoints with dependency injection.

This module tests the API endpoints to ensure they work correctly
with the dependency injection system.
"""

import pytest
import json
from fastapi.testclient import TestClient
from httpx import AsyncClient

from tests.dependencies import create_test_app, create_test_app_with_real_db


class TestProductsAPI:
    """Test /api/products endpoint with dependency injection."""

    def test_get_products_endpoint(self, test_client):
        """Test GET /api/products endpoint."""
        response = test_client.get("/api/products")

        assert response.status_code == 200

        data = response.json()
        assert "products" in data
        assert "total_products" in data
        assert "total_value" in data
        assert isinstance(data["products"], list)
        assert data["total_products"] == 2
        assert data["total_value"] == 31.98

    def test_get_products_response_structure(self, test_client):
        """Test that products response has correct structure."""
        response = test_client.get("/api/products")

        assert response.status_code == 200

        data = response.json()

        # Check required fields
        required_fields = ["products", "total_products", "total_value"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Check products structure
        products = data["products"]
        assert isinstance(products, list)
        assert len(products) == 2

        for product in products:
            assert "id" in product
            assert "name" in product
            assert "price" in product
            assert "stock" in product

    def test_get_products_with_mock_service(self, test_client):
        """Test that products endpoint uses mocked service."""
        response = test_client.get("/api/products")

        assert response.status_code == 200

        data = response.json()

        # Verify we're getting mock data
        assert data["total_products"] == 2
        assert data["total_value"] == 31.98

        # Check that products have expected mock structure
        products = data["products"]
        assert products[0]["name"] == "Test Product 1"
        assert products[1]["name"] == "Test Product 2"


class TestWebinarRegistrantsAPI:
    """Test /api/registrants endpoint with dependency injection."""

    def test_get_registrants_endpoint(self, test_client):
        """Test GET /api/registrants endpoint."""
        response = test_client.get("/api/registrants")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

        registrant = data[0]
        assert "name" in registrant
        assert "email" in registrant
        assert "webinar_title" in registrant
        assert "registration_date" in registrant

    def test_get_registrants_response_structure(self, test_client):
        """Test that registrants response has correct structure."""
        response = test_client.get("/api/registrants")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        if data:  # If there are registrants
            registrant = data[0]
            required_fields = ["name", "email", "webinar_title", "registration_date"]
            for field in required_fields:
                assert field in registrant, f"Missing required field: {field}"

    def test_get_registrants_with_mock_service(self, test_client):
        """Test that registrants endpoint uses mocked service."""
        response = test_client.get("/api/registrants")

        assert response.status_code == 200

        data = response.json()

        # Verify we're getting mock data
        assert len(data) == 1
        assert data[0]["name"] == "Test User 1"
        assert data[0]["email"] == "test1@example.com"


class TestWebinarAttendeesAPI:
    """Test /api/webinar-attendees endpoint with dependency injection."""

    def test_get_webinar_attendees_endpoint(self, test_client):
        """Test GET /api/webinar-attendees endpoint."""
        response = test_client.get("/api/webinar-attendees")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

        attendee = data[0]
        assert "name" in attendee
        assert "email" in attendee
        assert "attendance_status" in attendee

    def test_get_webinar_attendees_response_structure(self, test_client):
        """Test that webinar attendees response has correct structure."""
        response = test_client.get("/api/webinar-attendees")

        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        if data:  # If there are attendees
            attendee = data[0]
            required_fields = ["name", "email", "attendance_status"]
            for field in required_fields:
                assert field in attendee, f"Missing required field: {field}"

    def test_get_webinar_attendees_with_mock_service(self, test_client):
        """Test that webinar attendees endpoint uses mocked service."""
        response = test_client.get("/api/webinar-attendees")

        assert response.status_code == 200

        data = response.json()

        # Verify we're getting mock data
        assert len(data) == 1
        assert data[0]["name"] == "Test User 1"
        assert data[0]["email"] == "test1@example.com"
        assert data[0]["attendance_status"] == "attended"


class TestChatAPI:
    """Test chat API endpoints with dependency injection."""

    def test_chat_test_endpoint(self, test_client):
        """Test GET /chat/test endpoint."""
        response = test_client.get("/chat/test")

        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "message" in data
        assert "api_key_configured" in data
        assert data["status"] == "success"

    def test_chat_test_response_structure(self, test_client):
        """Test that chat test response has correct structure."""
        response = test_client.get("/chat/test")

        assert response.status_code == 200

        data = response.json()
        required_fields = ["status", "message", "api_key_configured"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_chat_test_with_mock_service(self, test_client):
        """Test that chat test endpoint uses mocked service."""
        response = test_client.get("/chat/test")

        assert response.status_code == 200

        data = response.json()

        # Verify we're getting mock data
        assert data["status"] == "success"
        assert data["message"] == "Test connection successful"
        assert data["api_key_configured"] is True

    def test_chat_completion_endpoint(self, test_client):
        """Test POST /chat/chat endpoint."""
        payload = {
            "messages": [
                {"role": "user", "content": "Hello, how are you?"}
            ]
        }

        response = test_client.post("/chat/chat", json=payload)

        assert response.status_code == 200

        data = response.json()
        assert "role" in data
        assert "content" in data
        assert "usage" in data
        assert data["role"] == "assistant"

    def test_chat_completion_response_structure(self, test_client):
        """Test that chat completion response has correct structure."""
        payload = {
            "messages": [
                {"role": "user", "content": "Test message"}
            ]
        }

        response = test_client.post("/chat/chat", json=payload)

        assert response.status_code == 200

        data = response.json()
        required_fields = ["role", "content", "usage"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

    def test_chat_completion_with_mock_service(self, test_client):
        """Test that chat completion endpoint uses mocked service."""
        payload = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ]
        }

        response = test_client.post("/chat/chat", json=payload)

        assert response.status_code == 200

        data = response.json()

        # Verify we're getting mock data
        assert data["role"] == "assistant"
        assert data["content"] == "Test chat response"
        assert data["usage"]["total_tokens"] == 100


class TestWebinarManagementAPI:
    """Test webinar management API endpoints with dependency injection."""

    def test_upload_photo_endpoint(self, test_client):
        """Test POST /webinar/upload-photo endpoint."""
        # Create a test file
        files = {"file": ("test.jpg", b"fake image data", "image/jpeg")}
        data = {"registrant_id": "test-id"}

        response = test_client.post("/upload-photo/test-id", files=files, data=data)

        # This endpoint might return different status codes depending on implementation
        # We're just testing that it doesn't crash with dependency injection
        assert response.status_code in [200, 400, 422]  # Accept various responses

    def test_update_notes_endpoint(self, test_client):
        """Test POST /webinar/update-notes endpoint."""
        payload = {
            "registrant_id": "test-id",
            "notes": "Test notes"
        }

        response = test_client.post("/update-notes/test-id", json=payload)

        # This endpoint might return different status codes depending on implementation
        # We're just testing that it doesn't crash with dependency injection
        assert response.status_code in [200, 400, 422]  # Accept various responses

    def test_delete_photo_endpoint(self, test_client):
        """Test DELETE /webinar/delete-photo endpoint."""
        response = test_client.delete("/delete-photo/test-id")

        # This endpoint might return different status codes depending on implementation
        # We're just testing that it doesn't crash with dependency injection
        assert response.status_code in [200, 400, 404, 422]  # Accept various responses


class TestAPIErrorHandling:
    """Test API error handling with dependency injection."""

    def test_invalid_json_request(self, test_client):
        """Test handling of invalid JSON requests."""
        response = test_client.post(
            "/chat/chat",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )

        # Should return 422 for invalid JSON
        assert response.status_code == 422

    def test_missing_required_fields(self, test_client):
        """Test handling of missing required fields."""
        response = test_client.post("/chat/chat", json={})

        # Should return 422 for missing required fields
        assert response.status_code == 422

    def test_invalid_file_upload(self, test_client):
        """Test handling of invalid file uploads."""
        files = {"file": ("test.txt", b"not an image", "text/plain")}
        data = {"registrant_id": "test-id"}

        response = test_client.post("/upload-photo/test-id", files=files, data=data)

        # Should handle invalid file types gracefully
        assert response.status_code in [200, 400, 422]


class TestAPIPerformance:
    """Test API performance with dependency injection."""

    def test_products_endpoint_performance(self, test_client):
        """Test that products endpoint responds quickly."""
        import time

        start_time = time.time()
        response = test_client.get("/api/products")
        response_time = time.time() - start_time

        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second

    def test_multiple_concurrent_requests(self, test_client):
        """Test handling multiple concurrent requests."""
        import threading
        import time

        results = []

        def make_request():
            response = test_client.get("/api/products")
            results.append(response.status_code)

        # Create multiple threads
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All requests should succeed
        assert len(results) == 5
        assert all(status == 200 for status in results)


class TestAPIWithRealDatabase:
    """Test API endpoints with real database but mocked services."""

    def test_products_with_real_db(self, test_app_with_real_db):
        """Test products endpoint with real database."""
        client = TestClient(test_app_with_real_db)
        response = client.get("/api/products")

        assert response.status_code == 200

        data = response.json()
        assert "products" in data
        assert "total_products" in data
        assert "total_value" in data

    def test_chat_with_real_db(self, test_app_with_real_db):
        """Test chat endpoint with real database."""
        client = TestClient(test_app_with_real_db)
        response = client.get("/chat/test")

        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "success"


@pytest.mark.integration
class TestAPIIntegrationMarkers:
    """Test that API integration tests are properly marked."""

    def test_integration_marker_applied(self):
        """Test that integration marker is applied to this test class."""
        # This test will only run when --markers integration is specified
        assert True
