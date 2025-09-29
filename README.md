# FastOpp Blog

This is the official blog for FastOpp, a FastAPI starter package for students prototyping AI web applications.

## About FastOpp

FastOpp provides pre-built admin components that give FastAPI functionality comparable to Django for AI-first applications. It's designed to bridge the gap between Django's ease of use and FastAPI's modern async capabilities.

## Blog Features

- **Modern Design**: Built with Tailwind CSS and matching FastOpp's visual theme
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Fast Loading**: Optimized for performance with Jekyll static site generation
- **SEO Friendly**: Built-in SEO optimization with jekyll-seo-tag
- **GitHub Pages Ready**: Automatically deploys to GitHub Pages

## Local Development

> **⚠️ Important**: This blog uses GitHub Pages for deployment, which has specific version requirements. See [SETUP.md](SETUP.md) for detailed setup instructions that ensure compatibility.

### Quick Start

1. **Install Ruby 3.3.4** (matches GitHub Pages exactly)
   ```bash
   rbenv install 3.3.4
   rbenv local 3.3.4
   ```

2. **Install dependencies**
   ```bash
   bundle install
   ```

3. **Start development server**
   ```bash
   bundle exec jekyll serve
   ```

4. **Visit the site**
   Open [http://localhost:4000/fastopp/](http://localhost:4000/fastopp/) in your browser

### Why Ruby 3.3.4?

GitHub Pages uses locked gem versions for security and stability. Using the exact same Ruby version (3.3.4) and gem versions ensures your local environment matches GitHub Pages exactly, preventing build failures and compatibility issues.

**Current GitHub Pages versions**: [https://pages.github.com/versions.json](https://pages.github.com/versions.json)

For detailed setup instructions, troubleshooting, and development workflow, see [SETUP.md](SETUP.md).

## Writing Posts

To add a new blog post:

1. Create a new file in `_posts/` with the format `YYYY-MM-DD-title.md`
2. Add the required front matter:
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   date: 2025-09-29
   author: Craig Oda
   image: /assets/images/your-image.webp
   excerpt: "Brief description of your post"
   ---
   ```
3. Write your content in Markdown
4. Commit and push to the `blog-do-not-merge` branch

## Deployment

This blog is automatically deployed to GitHub Pages when changes are pushed to the `blog-do-not-merge` branch.

The site will be available at: `https://oppkey.github.io/fastopp/`

## Contributing

We welcome contributions to the FastOpp blog! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide for detailed instructions on:

- Setting up your development environment
- Contributing to blog posts and documentation
- Understanding the repository structure
- Following our coding standards and guidelines

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

For detailed setup and contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

## License

This blog is part of the FastOpp project and follows the same MIT license. See the [main FastOpp repository](https://github.com/Oppkey/FastOpp) for details.

## Links

- **FastOpp Repository**: [https://github.com/Oppkey/FastOpp](https://github.com/Oppkey/FastOpp)
- **Live Blog**: [https://oppkey.github.io/fastopp/](https://oppkey.github.io/fastopp/)
- **Issues**: [Report issues or request features](https://github.com/Oppkey/FastOpp/issues)
