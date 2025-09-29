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

To run this blog locally for development:

### Prerequisites

1. **Install Ruby and Jekyll**
   ```bash
   # Install Ruby (if not already installed)
   # On macOS with Homebrew:
   brew install ruby
   
   # Install Jekyll and Bundler
   gem install jekyll bundler
   ```

2. **Install dependencies**
   ```bash
   bundle install
   ```

### Running the Development Server

3. **Start the development server**
   ```bash
   bundle exec jekyll serve
   ```

4. **Visit the site**
   Open [http://localhost:4000](http://localhost:4000) in your browser

### Troubleshooting

**Port already in use error:**
If you get "Address already in use" error:
```bash
# Find and kill the process using port 4000
lsof -ti:4000 | xargs kill

# Or use a different port
bundle exec jekyll serve --port 4001
```

**Sass deprecation warnings:**
The site uses modern Sass syntax to avoid deprecation warnings. If you see warnings, they're likely from the Minima theme and can be safely ignored.

**Auto-regeneration:**
The development server automatically regenerates the site when you make changes to files. No need to restart the server.

### Development Features

- **Live reload**: Changes are automatically reflected in the browser
- **Sass compilation**: Custom styles in `assets/main.scss` are automatically compiled
- **Markdown processing**: Posts and pages are processed with Kramdown
- **SEO optimization**: Built-in SEO tags and sitemap generation

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

We welcome contributions to the FastOpp blog! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This blog is part of the FastOpp project and follows the same MIT license. See the [main FastOpp repository](https://github.com/Oppkey/FastOpp) for details.

## Links

- **FastOpp Repository**: [https://github.com/Oppkey/FastOpp](https://github.com/Oppkey/FastOpp)
- **Live Blog**: [https://oppkey.github.io/fastopp/](https://oppkey.github.io/fastopp/)
- **Issues**: [Report issues or request features](https://github.com/Oppkey/FastOpp/issues)
