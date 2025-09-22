# Tests

This directory contains comprehensive test suites for the FastAPI application with dependency injection system.

## Test Structure

```text
tests/
├── __init__.py
├── conftest.py              # Shared pytest fixtures and configuration
├── dependencies.py          # Test dependency overrides and mock implementations
├── unit/                    # Unit tests for individual components
│   ├── test_services.py     # Service dependency injection tests
│   ├── test_config.py       # Configuration dependency tests
│   └── test_database.py     # Database dependency tests
├── integration/             # Integration tests for API endpoints
│   └── test_api.py          # API endpoint integration tests
├── state/                   # State management tests
│   └── test_oppdemo.py      # oppdemo.py state switching tests
├── performance/             # Performance and benchmark tests
│   └── test_benchmarks.py   # Performance benchmarks
├── test_ai_demo.py          # Legacy AI demo tests
└── test_formatting.py       # Legacy formatting tests
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **Service Dependencies**: Test dependency injection for ProductService, WebinarService, ChatService
- **Configuration Dependencies**: Test Settings class and configuration loading
- **Database Dependencies**: Test database engine, session factory, and session management

### Integration Tests (`tests/integration/`)
- **API Endpoints**: Test all API endpoints with dependency injection
- **Error Handling**: Test error handling and edge cases
- **Response Validation**: Test response structure and data validation

### State Management Tests (`tests/state/`)
- **oppdemo.py Integration**: Test state switching with dependency injection
- **State Detection**: Test framework vs demo state detection
- **File Structure**: Test state file structure integrity

### Performance Tests (`tests/performance/`)
- **Benchmarks**: Performance benchmarks for dependency injection
- **Concurrent Load**: Test performance under concurrent load
- **Memory Usage**: Test memory usage and potential leaks
- **Regression Testing**: Baseline performance for regression detection

## Running Tests

### Prerequisites

Install test dependencies:

```bash
uv add --group test pytest pytest-asyncio pytest-cov pytest-mock pytest-timeout pytest-xdist
```

### Basic Test Execution

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run with coverage report
uv run pytest --cov=dependencies --cov=services --cov=routes --cov-report=html

# Run specific test categories
uv run pytest -m unit          # Unit tests only
uv run pytest -m integration   # Integration tests only
uv run pytest -m state         # State management tests only
uv run pytest -m performance   # Performance tests only
```

### Advanced Test Execution

```bash
# Run tests in parallel
uv run pytest -n auto

# Run tests with timeout
uv run pytest --timeout=300

# Run specific test files
uv run pytest tests/unit/test_services.py
uv run pytest tests/integration/test_api.py

# Run tests matching a pattern
uv run pytest -k "test_product"

# Run tests with specific markers
uv run pytest -m "unit and not slow"
```

### Test Configuration

The test configuration is defined in `pytest.ini`:

- **Test Discovery**: Automatically finds tests in `tests/` directory
- **Markers**: Categorizes tests (unit, integration, state, performance, etc.)
- **Async Support**: Configured for async test execution
- **Output Options**: Verbose output with color and timing information
- **Timeout**: 300-second timeout for long-running tests

## Test Dependencies

### Mock Implementations

The test suite includes comprehensive mock implementations:

- **MockProductService**: Mock implementation of ProductService
- **MockWebinarService**: Mock implementation of WebinarService  
- **MockChatService**: Mock implementation of ChatService
- **TestSettings**: Test-specific configuration settings

### Test Fixtures

Common fixtures available in `conftest.py`:

- **Database Fixtures**: `test_db_session`, `test_db_engine`
- **Application Fixtures**: `test_app`, `test_app_with_real_db`
- **Client Fixtures**: `test_client`, `async_test_client`
- **Service Fixtures**: `mock_product_service`, `mock_webinar_service`, `mock_chat_service`
- **Data Fixtures**: `sample_products`, `sample_users`, `sample_webinar_registrants`

### Dependency Overrides

The test system uses FastAPI's dependency override system:

```python
# Override dependencies for testing
app.dependency_overrides[get_settings] = lambda: test_settings
app.dependency_overrides[get_db_session] = get_test_db_session
app.dependency_overrides[get_product_service] = get_mock_product_service
```

## Test Data

### Sample Data Fixtures

- **Products**: Test product data with realistic values
- **Users**: Test user data with different permission levels
- **Webinar Registrants**: Test webinar registration data
- **Authentication**: Test JWT tokens and authentication headers

### Database Testing

- **In-Memory SQLite**: Fast, isolated database for testing
- **Real Database**: Option to test with real database operations
- **Data Cleanup**: Automatic cleanup after each test

## Performance Testing

### Benchmarks

- **Service Instantiation**: Measure dependency injection performance
- **API Response Times**: Measure endpoint response times
- **Concurrent Load**: Test performance under concurrent requests
- **Memory Usage**: Monitor memory usage and potential leaks

### Regression Testing

- **Baseline Performance**: Establish performance baselines
- **Threshold Monitoring**: Alert on performance regressions
- **Load Testing**: Test system behavior under load

## Continuous Integration

### GitHub Actions Integration

The test suite is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    uv add --group test
    uv run pytest --cov=dependencies --cov=services --cov=routes --cov-report=xml
```

### Test Reports

- **Coverage Reports**: HTML and XML coverage reports
- **Performance Reports**: Timing and benchmark results
- **Test Results**: Detailed test execution results

## Debugging Tests

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Errors**: Check database connection and permissions
3. **Async Issues**: Use `pytest-asyncio` for async tests
4. **Mock Issues**: Verify mock implementations are correct

### Debug Commands

```bash
# Run tests with debug output
uv run pytest -v -s

# Run specific test with debug
uv run pytest -v -s tests/unit/test_services.py::TestProductServiceDependency::test_get_product_service_returns_instance

# Run tests with pdb debugger
uv run pytest --pdb

# Run tests with detailed output
uv run pytest -vvv
```

## Best Practices

### Writing Tests

1. **Use Descriptive Names**: Test names should clearly describe what they test
2. **Arrange-Act-Assert**: Structure tests with clear setup, execution, and verification
3. **Mock External Dependencies**: Use mocks for external services and databases
4. **Test Edge Cases**: Include tests for error conditions and edge cases
5. **Keep Tests Independent**: Each test should be able to run independently

### Test Organization

1. **Group Related Tests**: Use test classes to group related functionality
2. **Use Fixtures**: Leverage pytest fixtures for common setup
3. **Mark Tests Appropriately**: Use markers to categorize tests
4. **Document Test Purpose**: Add docstrings explaining test purpose

### Performance Considerations

1. **Use In-Memory Databases**: For faster test execution
2. **Mock External Services**: Avoid network calls in tests
3. **Clean Up Resources**: Ensure proper cleanup in test teardown
4. **Monitor Test Duration**: Keep individual tests fast

## Legacy Tests

The following legacy test files are maintained for backward compatibility:

- `test_ai_demo.py` - Original AI demo functionality tests
- `test_formatting.py` - Original message formatting tests

These tests require the FastAPI application to be running on `localhost:8000` and the `OPENROUTER_API_KEY` environment variable to be set.

## Future Improvements

- [ ] Add visual test reporting
- [ ] Implement automated performance monitoring
- [ ] Add test data factories
- [ ] Create mock service implementations for external APIs
- [ ] Add end-to-end testing capabilities
- [ ] Implement test result analytics 