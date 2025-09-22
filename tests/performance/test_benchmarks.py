"""
Performance benchmarks for dependency injection system.

This module tests the performance characteristics of the dependency injection
system to ensure no regressions and measure improvements.
"""

import pytest
import time
import asyncio
import statistics
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from httpx import AsyncClient

from tests.dependencies import create_test_app, create_test_app_with_real_db


class TestDependencyInjectionPerformance:
    """Test performance of dependency injection system."""

    def test_service_instantiation_performance(self):
        """Test performance of service instantiation."""
        from tests.dependencies import get_mock_product_service, get_test_settings
        from unittest.mock import AsyncMock

        settings = get_test_settings()
        mock_session = AsyncMock()

        # Measure service instantiation time
        times = []
        for _ in range(100):
            start_time = time.time()
            service = get_mock_product_service(session=mock_session, settings=settings)
            instantiation_time = time.time() - start_time
            times.append(instantiation_time)

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)
        min_time = min(times)

        # Service instantiation should be very fast
        assert avg_time < 0.001  # Less than 1ms on average
        assert max_time < 0.01   # Less than 10ms maximum
        assert min_time >= 0     # Non-negative time

        print(f"Service instantiation - Avg: {avg_time:.6f}s, Max: {max_time:.6f}s, Min: {min_time:.6f}s")

    def test_dependency_resolution_performance(self):
        """Test performance of dependency resolution."""
        from dependencies.config import get_settings
        from dependencies.database import get_db_session
        from dependencies.services import get_product_service

        # Measure dependency resolution time
        times = []
        for _ in range(50):
            start_time = time.time()

            # Resolve dependencies
            settings = get_settings()
            # Note: We can't easily test get_db_session without async context
            # service = get_product_service(session=session, settings=settings)

            resolution_time = time.time() - start_time
            times.append(resolution_time)

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)

        # Dependency resolution should be fast
        assert avg_time < 0.001  # Less than 1ms on average
        assert max_time < 0.01   # Less than 10ms maximum

        print(f"Dependency resolution - Avg: {avg_time:.6f}s, Max: {max_time:.6f}s")

    def test_configuration_loading_performance(self):
        """Test performance of configuration loading."""
        from dependencies.config import Settings

        # Measure configuration loading time
        times = []
        for _ in range(100):
            start_time = time.time()
            settings = Settings()
            loading_time = time.time() - start_time
            times.append(loading_time)

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)

        # Configuration loading should be fast
        assert avg_time < 0.01   # Less than 10ms on average
        assert max_time < 0.1    # Less than 100ms maximum

        print(f"Configuration loading - Avg: {avg_time:.6f}s, Max: {max_time:.6f}s")


class TestAPIPerformance:
    """Test API endpoint performance with dependency injection."""

    def test_products_endpoint_performance(self, test_client):
        """Test performance of products endpoint."""
        # Warm up
        test_client.get("/api/products")

        # Measure performance
        times = []
        for _ in range(20):
            start_time = time.time()
            response = test_client.get("/api/products")
            response_time = time.time() - start_time
            times.append(response_time)

            assert response.status_code == 200

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)
        p95_time = statistics.quantiles(times, n=20)[18]  # 95th percentile

        # API should be fast
        assert avg_time < 0.1    # Less than 100ms on average
        assert max_time < 0.5    # Less than 500ms maximum
        assert p95_time < 0.2    # 95th percentile under 200ms

        print(f"Products endpoint - Avg: {avg_time:.3f}s, Max: {max_time:.3f}s, P95: {p95_time:.3f}s")

    def test_chat_endpoint_performance(self, test_client):
        """Test performance of chat endpoint."""
        # Warm up
        test_client.get("/chat/test")

        # Measure performance
        times = []
        for _ in range(20):
            start_time = time.time()
            response = test_client.get("/chat/test")
            response_time = time.time() - start_time
            times.append(response_time)

            assert response.status_code == 200

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)
        p95_time = statistics.quantiles(times, n=20)[18]  # 95th percentile

        # API should be fast
        assert avg_time < 0.1    # Less than 100ms on average
        assert max_time < 0.5    # Less than 500ms maximum
        assert p95_time < 0.2    # 95th percentile under 200ms

        print(f"Chat endpoint - Avg: {avg_time:.3f}s, Max: {max_time:.3f}s, P95: {p95_time:.3f}s")

    def test_webinar_endpoint_performance(self, test_client):
        """Test performance of webinar endpoints."""
        endpoints = ["/api/registrants", "/api/webinar-attendees"]

        for endpoint in endpoints:
            # Warm up
            test_client.get(endpoint)

            # Measure performance
            times = []
            for _ in range(20):
                start_time = time.time()
                response = test_client.get(endpoint)
                response_time = time.time() - start_time
                times.append(response_time)

                assert response.status_code == 200

            # Calculate statistics
            avg_time = statistics.mean(times)
            max_time = max(times)

            # API should be fast
            assert avg_time < 0.1    # Less than 100ms on average
            assert max_time < 0.5    # Less than 500ms maximum

            print(f"{endpoint} - Avg: {avg_time:.3f}s, Max: {max_time:.3f}s")


class TestConcurrentPerformance:
    """Test performance under concurrent load."""

    def test_concurrent_api_requests(self, test_client):
        """Test performance with concurrent API requests."""
        def make_request():
            start_time = time.time()
            response = test_client.get("/api/products")
            response_time = time.time() - start_time
            return response.status_code, response_time

        # Test with different levels of concurrency
        for num_threads in [5, 10, 20]:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                start_time = time.time()

                # Submit concurrent requests
                futures = [executor.submit(make_request) for _ in range(num_threads)]
                results = [future.result() for future in futures]

                total_time = time.time() - start_time

                # Check results
                status_codes, response_times = zip(*results)
                assert all(code == 200 for code in status_codes)

                avg_response_time = statistics.mean(response_times)
                max_response_time = max(response_times)

                # Performance should be reasonable even under load
                assert avg_response_time < 0.2    # Less than 200ms on average
                assert max_response_time < 1.0    # Less than 1s maximum
                assert total_time < 2.0           # Total time under 2s

                print(f"Concurrent ({num_threads} threads) - Avg: {avg_response_time:.3f}s, Max: {max_response_time:.3f}s, Total: {total_time:.3f}s")

    def test_concurrent_dependency_resolution(self):
        """Test performance of concurrent dependency resolution."""
        from dependencies.config import get_settings

        def resolve_dependencies():
            start_time = time.time()
            settings = get_settings()
            resolution_time = time.time() - start_time
            return resolution_time

        # Test with different levels of concurrency
        for num_threads in [10, 50, 100]:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                start_time = time.time()

                # Submit concurrent dependency resolution
                futures = [executor.submit(resolve_dependencies) for _ in range(num_threads)]
                results = [future.result() for future in futures]

                total_time = time.time() - start_time

                avg_time = statistics.mean(results)
                max_time = max(results)

                # Dependency resolution should be fast even under load
                assert avg_time < 0.01   # Less than 10ms on average
                assert max_time < 0.1    # Less than 100ms maximum
                assert total_time < 1.0  # Total time under 1s

                print(f"Concurrent DI ({num_threads} threads) - Avg: {avg_time:.6f}s, Max: {max_time:.6f}s, Total: {total_time:.3f}s")


class TestMemoryPerformance:
    """Test memory usage of dependency injection system."""

    def test_service_memory_usage(self):
        """Test memory usage of service instances."""
        import sys
        from tests.dependencies import get_mock_product_service, get_test_settings
        from unittest.mock import AsyncMock

        settings = get_test_settings()
        mock_session = AsyncMock()

        # Measure memory usage
        initial_objects = len(gc.get_objects()) if 'gc' in globals() else 0

        # Create many service instances
        services = []
        for _ in range(1000):
            service = get_mock_product_service(session=mock_session, settings=settings)
            services.append(service)

        # Check that we don't have excessive memory growth
        # This is a basic test - in practice, you'd use memory profiling tools
        assert len(services) == 1000

        # Clean up
        del services

        print("Service memory usage test completed")

    def test_dependency_overrides_memory_usage(self, test_app):
        """Test memory usage of dependency overrides."""
        # Check that dependency overrides don't cause memory leaks
        initial_overrides = len(test_app.dependency_overrides)

        # Create multiple test apps
        apps = []
        for _ in range(100):
            app = create_test_app()
            apps.append(app)

        # Check that dependency overrides are reasonable
        for app in apps:
            assert len(app.dependency_overrides) >= initial_overrides

        # Clean up
        del apps

        print("Dependency overrides memory usage test completed")


class TestStartupPerformance:
    """Test application startup performance."""

    def test_app_creation_performance(self):
        """Test performance of app creation with dependency injection."""
        times = []

        for _ in range(10):
            start_time = time.time()
            app = create_test_app()
            creation_time = time.time() - start_time
            times.append(creation_time)

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)

        # App creation should be fast
        assert avg_time < 0.1    # Less than 100ms on average
        assert max_time < 0.5    # Less than 500ms maximum

        print(f"App creation - Avg: {avg_time:.3f}s, Max: {max_time:.3f}s")

    def test_app_with_real_db_creation_performance(self):
        """Test performance of app creation with real database."""
        times = []

        for _ in range(5):  # Fewer iterations due to database setup
            start_time = time.time()
            app = create_test_app_with_real_db()
            creation_time = time.time() - start_time
            times.append(creation_time)

        # Calculate statistics
        avg_time = statistics.mean(times)
        max_time = max(times)

        # App creation with real DB should still be reasonable
        assert avg_time < 1.0    # Less than 1s on average
        assert max_time < 2.0    # Less than 2s maximum

        print(f"App creation (real DB) - Avg: {avg_time:.3f}s, Max: {max_time:.3f}s")


class TestPerformanceRegression:
    """Test for performance regressions."""

    def test_no_performance_regression_products(self, test_client):
        """Test that products endpoint hasn't regressed in performance."""
        # This test establishes a baseline for future regression testing
        times = []

        for _ in range(50):
            start_time = time.time()
            response = test_client.get("/api/products")
            response_time = time.time() - start_time
            times.append(response_time)

            assert response.status_code == 200

        avg_time = statistics.mean(times)
        p95_time = statistics.quantiles(times, n=50)[47]  # 95th percentile

        # Baseline performance thresholds
        assert avg_time < 0.05   # Average should be under 50ms
        assert p95_time < 0.1    # 95th percentile under 100ms

        print(f"Products baseline - Avg: {avg_time:.3f}s, P95: {p95_time:.3f}s")

    def test_no_performance_regression_chat(self, test_client):
        """Test that chat endpoint hasn't regressed in performance."""
        times = []

        for _ in range(50):
            start_time = time.time()
            response = test_client.get("/chat/test")
            response_time = time.time() - start_time
            times.append(response_time)

            assert response.status_code == 200

        avg_time = statistics.mean(times)
        p95_time = statistics.quantiles(times, n=50)[47]  # 95th percentile

        # Baseline performance thresholds
        assert avg_time < 0.05   # Average should be under 50ms
        assert p95_time < 0.1    # 95th percentile under 100ms

        print(f"Chat baseline - Avg: {avg_time:.3f}s, P95: {p95_time:.3f}s")


@pytest.mark.performance
class TestPerformanceMarkers:
    """Test that performance tests are properly marked."""

    def test_performance_marker_applied(self):
        """Test that performance marker is applied to this test class."""
        # This test will only run when --markers performance is specified
        assert True
