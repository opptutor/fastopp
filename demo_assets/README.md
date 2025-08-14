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

## Contributing to Demo

Developers work in the project root directory. When enhancements are working and ready to submit, save your work to this backup location.

### Development Workflow

1. **Create Development Branch**: Create a new branch for your feature or enhancement
   - Use descriptive branch names: `feature/ai-chat-enhancement` or `fix/webinar-registration-bug`
2. **Work in Project Root**: All development happens in the main project directory
3. **Test Your Changes**: Ensure your demo enhancements work correctly
   - Test locally before saving
   - Verify all demo pages still function
4. **Save Your Work**: When ready to submit, run the save command to add your changes to the `demo_assets/` folder which is the source of truth of the demo.
5. **Commit and Push**: Commit your changes with descriptive messages and push to your branch
6. **Create Pull Request**: Create a pull request with clear description of changes
   - Include screenshots for UI changes
   - List any new dependencies or configuration changes
7. **Review Process**: Project manager will either review and assign to reviewer
8. **Engage in Discussion**: Look for comments and engage in discussion
   - Address all review comments promptly
   - Ask for clarification if needed
9. **Make Changes**: Make changes if requested during review
   - Push additional commits to the same branch
   - The PR will automatically update
10. **Merge**: Project manager will merge into main after approval

### Save Command

```bash
uv run python oppman.py demo save
```

## Save Information

- **Save Date**: 2025-08-14 11:03:51
- **Files Saved**: 36 files
- **Save Command**: `uv run python oppman.py demo save`
