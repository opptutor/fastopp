# Static Files Directory

This directory contains all static assets for the FastAPI application.

## Directory Structure

```
static/
├── images/          # Image files (PNG, JPG, SVG, etc.)
│   ├── logo.png     # Application logo
│   ├── hero-image.jpg # Hero section background
│   └── icons/       # Icon files
│       ├── image-icon.png
│       ├── css-icon.png
│       └── js-icon.png
├── css/             # Stylesheet files
│   └── styles.css   # Main stylesheet
├── js/              # JavaScript files
│   └── main.js      # Main JavaScript file
└── README.md        # This file
```

## Usage in Templates

### Images

```html
<!-- Basic image -->
<img src="{{ url_for('static', path='/images/logo.png') }}" alt="Logo">

<!-- With error handling -->
<img src="{{ url_for('static', path='/images/hero-image.jpg') }}" 
     alt="Hero Image"
     onerror="this.src='https://via.placeholder.com/400x300'">
```

### CSS

```html
<!-- Link to stylesheet -->
<link rel="stylesheet" href="{{ url_for('static', path='/css/styles.css') }}">
```

### JavaScript

```html
<!-- Include JavaScript file -->
<script src="{{ url_for('static', path='/js/main.js') }}"></script>
```

## FastAPI Configuration

The static files are served through FastAPI's `StaticFiles` middleware in `main.py`:

```python
from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="static"), name="static")
```

## Best Practices

1. **File Organization**: Keep files organized by type (images, css, js)
2. **Naming**: Use descriptive, lowercase names with hyphens
3. **Optimization**: Optimize images and minify CSS/JS for production
4. **Caching**: Consider adding cache headers for production
5. **Error Handling**: Use `onerror` attributes for images that might not exist

## Adding New Files

1. Place your file in the appropriate subdirectory
2. Reference it in your templates using `url_for('static', path='/path/to/file')`
3. Update this README if adding new directories or file types 