# Development Setup

This guide helps you set up a local development environment that matches GitHub Pages exactly.

## Prerequisites

- [rbenv](https://github.com/rbenv/rbenv) for Ruby version management
- [Bundler](https://bundler.io/) for gem dependency management

## Running Jekyll Locally

### 1. Install the Correct Ruby Version

GitHub Pages uses **Ruby 3.3.4**. Install it with rbenv:

```bash
rbenv install 3.3.4
rbenv local 3.3.4
```

### 2. Install Dependencies

Install the exact same gem versions that GitHub Pages uses:

```bash
bundle install
```

This will install all dependencies including:
- **Jekyll 3.10.0** (vs 4.3.4+ locally)
- **Sass 3.7.4** (vs modern Sass versions)
- **github-pages 232** (locks all versions to match GitHub Pages)

### 3. Build and Serve

```bash
# Build the site
bundle exec jekyll build

# Serve locally with auto-reload
bundle exec jekyll serve

# Or serve in background
bundle exec jekyll serve --detach
```

The site will be available at `http://localhost:4000/fastopp/`

## Why This Matters

GitHub Pages uses locked gem versions for security and stability. Using newer versions locally can cause:

- **Build failures** on GitHub Actions
- **SCSS syntax errors** (modern `@use` syntax vs older `@import`)
- **Color function incompatibilities** (`color.scale()` vs `lighten()`/`darken()`)

## GitHub Pages Versions

Current versions used by GitHub Pages: [https://pages.github.com/versions.json](https://pages.github.com/versions.json)

Key versions:
- **Ruby**: 3.3.4
- **Jekyll**: 3.10.0
- **Sass**: 3.7.4
- **github-pages**: 232

## Troubleshooting

### SCSS Syntax Errors

If you see errors like:
```
Invalid CSS after "...or-light: color": expected selector or at-rule, was ".scale($grey-co..."
```

This means you're using modern Sass syntax that's incompatible with GitHub Pages. Use:
- `@import` instead of `@use`
- `lighten()` and `darken()` instead of `color.scale()`

### Ruby Version Issues

If you get compilation errors, ensure you're using Ruby 3.3.4:

```bash
ruby --version  # Should show 3.3.4
rbenv local 3.3.4  # Set local version
```

### Gem Installation Issues

If bundle install fails, try:

```bash
bundle clean --force
bundle install
```

## Development Workflow

1. **Always use the GitHub Pages versions** for local development
2. **Test builds locally** before pushing to GitHub
3. **Use compatible SCSS syntax** (avoid modern Sass features)
4. **Commit the Gemfile.lock** to ensure consistent versions

This ensures your local environment matches GitHub Pages exactly, preventing build failures and compatibility issues.
