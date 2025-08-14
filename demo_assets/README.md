# Demo Assets Save

This directory contains saved copies of all files required to restore the demonstration application functionality.

## Structure

- `templates/` - HTML templates for demo pages
- `static/` - Static assets (images, CSS, JS)
- `routes/` - Route handlers for demo functionality
- `services/` - Business logic services
- `models.py` - Data models
- `scripts/` - Sample data scripts

## Demo Pages

1. **AI Chat Demo** (`/ai-demo`) - Interactive chat with Llama 3.3 70B
2. **Dashboard Demo** (`/dashboard-demo`) - Product inventory dashboard with charts
3. **Design Demo** (`/design-demo`) - Marketing demo with HTMX interactions
4. **Webinar Demo** (`/webinar-demo`) - Webinar registrants showcase

## Technologies Used

- **Frontend**: Tailwind CSS, DaisyUI, Alpine.js, HTMX
- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **AI**: OpenRouter API with Llama 3.3 70B
- **Charts**: Chart.js

## Restoration

To restore demo files from this backup:

1. Copy templates from `demo_assets/templates/` to `templates/`
2. Copy static files from `demo_assets/static/` to `static/`
3. Copy route files from `demo_assets/routes/` to `routes/`
4. Copy service files from `demo_assets/services/` to `services/`
5. Copy `demo_assets/models.py` to root directory
6. Run sample data scripts from `demo_assets/scripts/`

## Dependencies

The demo requires these external dependencies:
- `sse_starlette` for streaming chat
- `markdown` for message formatting
- `httpx` for API calls
- `jinja2` for templating

## Save Information

- **Save Date**: 2025-08-14 13:08:49
- **Files Saved**: 36 files
- **Save Command**: `uv run python oppman.py demo save`
