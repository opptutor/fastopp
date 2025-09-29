# Contributing to FastOpp

Thank you for your interest in contributing to FastOpp! This guide will help you understand how to contribute to both the FastOpp application and the FastOpp blog.

## 🚀 FastOpp Application Contributions

### Getting Started

1. **Fork the Repository**
   - Go to [https://github.com/Oppkey/fastopp](https://github.com/Oppkey/fastopp)
   - Click the "Fork" button in the top right corner

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/fastopp.git
   cd fastopp
   ```

3. **Set Up Development Environment**
   ```bash
   # Install dependencies
   uv sync
   
   # Initialize database
   uv run python oppman.py init
   
   # Start development server
   uv run python oppman.py runserver
   ```

4. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Make Your Changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

6. **Test Your Changes**
   ```bash
   # Run tests
   uv run python -m pytest tests/
   
   # Check environment
   uv run python oppman.py env
   ```

7. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add your feature description"
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request**
   - Go to your forked repository on GitHub
   - Click "Compare & pull request"
   - **Base repository**: `Oppkey/fastopp`
   - **Base branch**: `main`
   - **Head repository**: `your-username/fastopp`
   - **Compare branch**: `feature/your-feature-name`

## 📝 FastOpp Blog Contributions

### Contributing to Documentation and Blog Posts

1. **Fork the Repository** (same as above)

2. **Create a Documentation Branch**
   ```bash
   git checkout -b docs/blog-contribution
   # or
   git checkout -b fix-blog-typo
   ```

3. **Make Your Changes**
   - **Blog posts**: Edit files in `_posts/`
   - **Pages**: Edit files in `_pages/`
   - **Assets**: Add images to `assets/images/`
   - **Styling**: Modify `assets/main.scss`

4. **Test Locally** (Optional)
   ```bash
   # Install Jekyll dependencies
   bundle install
   
   # Start Jekyll server
   bundle exec jekyll serve
   
   # Visit http://localhost:4000/fastopp/
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add blog post about FastAPI deployment"
   git push origin docs/blog-contribution
   ```

6. **Open a Pull Request**
   - **Base repository**: `Oppkey/fastopp`
   - **Base branch**: `docs/blog-only` ← **Important!**
   - **Head repository**: `your-username/fastopp`
   - **Compare branch**: `docs/blog-contribution`

## 🏗️ Repository Structure

```
fastopp/
├── main.py                 # FastAPI application
├── models.py               # Database models
├── oppman.py              # Management commands
├── oppdemo.py             # Demo management
├── _posts/                # Blog posts (Jekyll)
├── _pages/                # Blog pages (Jekyll)
├── _layouts/              # Blog layouts (Jekyll)
├── assets/                # Blog assets (Jekyll)
├── admin/                 # Admin panel
├── auth/                  # Authentication
├── routes/                # API routes
└── tests/                 # Test files
```

## 📋 Branch Guidelines

### Main Branches
- **`main`** - FastOpp application code (production-ready)
- **`docs/blog-only`** - Blog and documentation (GitHub Pages)

### Feature Branches
- **`feature/description`** - New features for FastOpp
- **`fix/description`** - Bug fixes for FastOpp
- **`docs/description`** - Documentation updates
- **`blog/description`** - Blog content updates

## 🎯 Contribution Types

### FastOpp Application
- **Bug fixes** - Fix issues in the FastAPI application
- **New features** - Add functionality to the admin panel, auth, etc.
- **Improvements** - Enhance existing features
- **Tests** - Add or improve test coverage
- **Documentation** - Update README, code comments, etc.

### FastOpp Blog
- **Blog posts** - Write tutorials, guides, announcements
- **Documentation** - Improve existing documentation
- **Tutorials** - Create step-by-step guides
- **Examples** - Add code examples and demos
- **Translations** - Translate content to other languages

## 📝 Writing Guidelines

### Blog Posts
- Use Markdown format
- Include front matter (title, date, author, etc.)
- Add images to `assets/images/`
- Keep posts focused and well-structured
- Include code examples where relevant

### Code Contributions
- Follow existing code style
- Add docstrings to functions and classes
- Include type hints where appropriate
- Write tests for new functionality
- Update documentation for new features

## 🚨 Important Notes

### Branch Protection
- **`docs/blog-only`** is protected and cannot be merged into `main`
- All changes to the blog must go through pull requests
- The blog branch is for documentation only

### Deployment
- **FastOpp application**: Deploy to your own hosting
- **FastOpp blog**: Automatically deploys to `https://oppkey.github.io/fastopp/`

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Follow the project's coding standards
- Be patient with newcomers

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check the README and existing docs
- **Community**: Join our community discussions

## 🎉 Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes
- Community acknowledgments

Thank you for contributing to FastOpp! 🚀
