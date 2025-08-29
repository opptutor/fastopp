# FastOpp Documentation

Welcome to the FastOpp documentation! This folder contains comprehensive guides for setting up, developing, and deploying your FastAPI application.

## 📚 Documentation Structure

The documentation has been consolidated from 22 files into 8 main comprehensive guides for better navigation and maintenance.

### Core Documentation

| File | Description | Use When You Need To... |
|------|-------------|-------------------------|
| **[SETUP.md](SETUP.md)** | Development environment setup | Set up your development environment, configure databases, manage environment variables |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Production deployment | Deploy to production, configure servers, set up SSL, manage backups |
| **[DATABASE.md](DATABASE.md)** | Database management | Work with migrations, troubleshoot database issues, optimize queries |
| **[AUTHENTICATION.md](AUTHENTICATION.md)** | User authentication | Implement auth systems, manage permissions, configure user groups |
| **[FEATURES.md](FEATURES.md)** | Application features | Use file uploads, AI chat, webinar management, admin interface |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Development workflow | Add new pages, debug issues, follow best practices, optimize performance |
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | System architecture | Understand the codebase structure, design patterns, technology stack |

### Planning and Roadmap

| File | Description | Use When You Need To... |
|------|-------------|-------------------------|
| **[plan/ROADMAP.md](plan/ROADMAP.md)** | Development roadmap | Understand project timeline, student recruitment, training plans |

## 🚀 Quick Start

### 1. Environment Setup
Start with [SETUP.md](SETUP.md) to configure your development environment:
- Install dependencies with `uv`
- Configure database connections
- Set up environment variables
- Choose between SQLite and PostgreSQL

### 2. Database Setup
Use [DATABASE.md](DATABASE.md) to get your database running:
- Initialize Alembic migrations
- Create and apply migrations
- Add sample data
- Troubleshoot common issues

### 3. Development Workflow
Follow [DEVELOPMENT.md](DEVELOPMENT.md) for best practices:
- Add new pages and features
- Follow MVS architecture patterns
- Test and debug your code
- Optimize performance

### 4. Feature Implementation
Explore [FEATURES.md](FEATURES.md) to understand available features:
- File upload and management
- AI chat integration
- Webinar management
- Admin interface customization

## 🏗️ Architecture Overview

FastOpp follows a **Model-View-Service (MVS)** architecture:

- **Models** (`models.py`): Data structures and database models
- **Views** (`routes/`): HTTP endpoints and request handling  
- **Services** (`services/`): Business logic and data operations

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design information.

## 🛠️ Key Technologies

- **Backend**: FastAPI with async/await support
- **Database**: SQLModel + Alembic migrations
- **Authentication**: FastAPI Users + custom JWT system
- **Admin Interface**: SQLAdmin with role-based permissions
- **Frontend**: HTMX + Alpine.js + Tailwind CSS
- **AI Integration**: OpenRouter API with streaming responses

## 📖 Reading Order

For new developers, we recommend reading the documentation in this order:

1. **[SETUP.md](SETUP.md)** - Get your environment running
2. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Understand the system design
3. **[DATABASE.md](DATABASE.md)** - Set up and manage your database
4. **[DEVELOPMENT.md](DEVELOPMENT.md)** - Learn development patterns
5. **[FEATURES.md](FEATURES.md)** - Explore available functionality
6. **[AUTHENTICATION.md](AUTHENTICATION.md)** - Configure user management
7. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy to production

## 🔧 Common Tasks

### Adding a New Page
See [DEVELOPMENT.md](DEVELOPMENT.md) for step-by-step instructions on:
- Creating new templates
- Adding routes
- Updating navigation
- Styling with Tailwind CSS

### Database Migrations
Use [DATABASE.md](DATABASE.md) to:
- Create new models
- Generate migrations
- Apply database changes
- Troubleshoot migration issues

### File Uploads
Check [FEATURES.md](FEATURES.md) for:
- Image upload configuration
- File storage management
- Security considerations
- Sample data generation

### Authentication Setup
Follow [AUTHENTICATION.md](AUTHENTICATION.md) to:
- Configure user groups
- Set up permissions
- Test authentication flows
- Customize admin access

## 🚨 Troubleshooting

### Common Issues
- **Database Connection**: Check [SETUP.md](SETUP.md) for environment configuration
- **Migration Errors**: See [DATABASE.md](DATABASE.md) for troubleshooting steps
- **HTMX Issues**: Refer to [DEVELOPMENT.md](DEVELOPMENT.md) for debugging tips
- **Permission Problems**: Check [AUTHENTICATION.md](AUTHENTICATION.md) for access control

### Getting Help
1. Check the relevant documentation section
2. Look for similar issues in the troubleshooting guides
3. Review the code examples and patterns
4. Check the [to_be_deleted/](to_be_deleted/) folder for historical information

## 📝 Contributing to Documentation

When updating documentation:

1. **Edit the appropriate consolidated file** - Don't create new files
2. **Update cross-references** - Keep links between documents current
3. **Add examples** - Include code samples and use cases
4. **Test instructions** - Verify that setup steps work correctly

## 📁 File Organization

```
docs/
├── README.md                    # This file - documentation overview
├── SETUP.md                     # Environment setup and configuration
├── DEPLOYMENT.md                # Production deployment guide
├── DATABASE.md                  # Database management and migrations
├── AUTHENTICATION.md            # User authentication and permissions
├── FEATURES.md                  # Application features and usage
├── DEVELOPMENT.md               # Development workflow and best practices
├── ARCHITECTURE.md              # System architecture overview
├── plan/                        # Project planning and roadmap
│   └── ROADMAP.md              # Development timeline and strategy
├── deployment/                  # Deployment-specific assets
├── images/                      # Documentation images
└── to_be_deleted/              # Outdated/consolidated files
    └── README.md                # Explanation of moved files
```

## 🔗 External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [FastAPI Users Documentation](https://fastapi-users.github.io/fastapi-users/)
- [HTMX Documentation](https://htmx.org/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

## 📊 Documentation Status

- ✅ **Consolidated**: 22 files → 8 main guides
- ✅ **Cross-referenced**: All documents link to related sections
- ✅ **Examples included**: Code samples and practical examples
- ✅ **Troubleshooting**: Common issues and solutions documented
- ✅ **Best practices**: Development patterns and standards

---

**Need help?** Start with [SETUP.md](SETUP.md) to get your environment running, then explore the other guides based on what you're working on.
