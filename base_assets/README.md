# Base Assets - Minimal FastAPI Application

This directory contains a minimal FastAPI application that serves as a starting point and helper for restoring the full demo application.

## Purpose

The `base_assets` directory provides:

1. **Minimal FastAPI Application**: A simple FastAPI app with no external dependencies
2. **Demo Restoration Guide**: Built-in HTML page with instructions on how to restore the full demo
3. **Quick Start**: Immediate working application that can be run with minimal setup

## Files

- `main.py` - Minimal FastAPI application with built-in HTML help page
- `README.md` - This documentation file

## Features

### Minimal FastAPI App

The `main.py` file contains a minimal FastAPI application that:

- **No Templates**: All HTML is generated in Python code
- **No External Dependencies**: Only requires FastAPI and uvicorn
- **Built-in Help**: Shows comprehensive instructions for restoring the full demo
- **Health Check**: Includes a `/health` endpoint for monitoring

### Built-in Help Page

The application serves a beautiful HTML page at `/` that includes:

- **Quick Restore Commands**: Step-by-step instructions
- **Demo Pages Overview**: What's available after restoration
- **Advanced Commands**: All available oppman.py commands
- **Default Credentials**: Login information
- **Important Notes**: Prerequisites and requirements

## Usage

### Quick Start

```bash
# Navigate to base_assets
cd base_assets

# Start the minimal application
uv run python main.py
```

### Access the Application

- **Main Page**: http://localhost:8000/
- **Health Check**: http://localhost:8000/health

### Restore Full Demo

Follow the instructions on the main page:

1. **Restore Demo Files**:
   ```bash
   uv run python oppman.py demo restore
   ```

2. **Initialize Database**:
   ```bash
   uv run python oppman.py init
   ```

3. **Start Full Application**:
   ```bash
   uv run python oppman.py runserver
   ```

## Demo Pages Available After Restoration

- **AI Chat Demo** (`/ai-demo`) - Interactive chat with Llama 3.3 70B
- **Dashboard Demo** (`/dashboard-demo`) - Product inventory dashboard
- **Design Demo** (`/design-demo`) - Marketing demo with HTMX
- **Webinar Demo** (`/webinar-demo`) - Webinar registrants showcase

## Technologies

### Base Application
- **FastAPI**: Modern Python web framework
- **Uvicorn**: ASGI server
- **HTML/CSS**: Built-in styling with modern design

### Full Demo (After Restoration)
- **Frontend**: Tailwind CSS, DaisyUI, Alpine.js, HTMX, Chart.js
- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **AI**: OpenRouter API with Llama 3.3 70B
- **Database**: SQLite with sample data

## Dependencies

### Base Application
```bash
uv add fastapi uvicorn
```

### Full Demo (After Restoration)
```bash
uv add fastapi sqlmodel sqlalchemy sse_starlette markdown httpx jinja2
```

## File Structure

```
base_assets/
├── main.py          # Minimal FastAPI application
└── README.md        # This documentation
```

## Comparison

| Feature | Base App | Full Demo |
|---------|----------|-----------|
| **Dependencies** | 2 packages | 8+ packages |
| **Routes** | 2 endpoints | 20+ endpoints |
| **Templates** | None (built-in HTML) | 10+ templates |
| **Database** | None | SQLite with sample data |
| **AI Features** | None | Llama 3.3 70B chat |
| **Admin Panel** | None | Full CRUD interface |
| **File Upload** | None | Photo management |
| **Authentication** | None | User management |

## Use Cases

### Base Application
- **Quick Start**: Immediate working application
- **Learning**: Simple FastAPI example
- **Testing**: Health check and basic functionality
- **Documentation**: Built-in help system

### Full Demo
- **Production Ready**: Complete web application
- **Feature Rich**: AI chat, dashboards, file uploads
- **Modern UI**: Tailwind CSS, Alpine.js, HTMX
- **Admin Interface**: Full CRUD operations

## Development

### Running Base App
```bash
cd base_assets
uv run python main.py
```

### Running Full Demo
```bash
# Restore demo files
uv run python oppman.py demo restore

# Initialize database
uv run python oppman.py init

# Start server
uv run python oppman.py runserver
```

## Notes

- The base application is completely self-contained
- No external files or templates required
- All HTML is generated in Python code
- Perfect for quick demos or learning FastAPI
- The full demo requires restoration from `demo_assets`
