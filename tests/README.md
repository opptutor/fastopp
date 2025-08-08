# Tests

This directory contains test scripts for the FastAPI application.

## Test Files

- `test_ai_demo.py` - Tests AI demo functionality and chat endpoints
- `test_formatting.py` - Tests message formatting with DaisyUI

## Running Tests

To run the tests, make sure your FastAPI application is running on `localhost:8000`:

```bash
# Run AI demo tests
python tests/test_ai_demo.py

# Run formatting tests  
python tests/test_formatting.py
```

## Requirements

- FastAPI application running on `localhost:8000`
- `OPENROUTER_API_KEY` environment variable set
- Required dependencies: `aiohttp`, `python-dotenv`

## Future Improvements

Consider adding:
- Unit tests using `pytest`
- Integration tests
- Automated test runner
- Test configuration files 