# Development vs Production Setup

## Quick Reference

| Component | Development | Production |
|-----------|-------------|------------|
| **Database** | SQLite + aiosqlite | PostgreSQL + asyncpg |
| **Server** | uvicorn --reload | Gunicorn + Uvicorn |
| **Process Manager** | None (manual) | Systemd |
| **Reverse Proxy** | None | Nginx |
| **SSL** | None | Let's Encrypt |
| **Logging** | Console | File + rotation |
| **Backups** | Manual | Automated |

## Database URLs

### Development
```python
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
```

### Production
```python
DATABASE_URL = "postgresql+asyncpg://user:password@localhost/fastopp_db"
```

## Server Commands

### Development
```bash
uv run uvicorn main:app --reload
```

### Production
```bash
# Start service
sudo systemctl start fastopp

# Check status
sudo systemctl status fastopp

# View logs
sudo journalctl -u fastopp -f
```

## Key Differences

### 1. **asyncpg vs aiosqlite**
- **Development**: `aiosqlite` for SQLite async operations
- **Production**: `asyncpg` for PostgreSQL async operations
- **Performance**: asyncpg is much faster for PostgreSQL

### 2. **Gunicorn + Uvicorn**
- **Development**: Single uvicorn process with auto-reload
- **Production**: Multiple worker processes managed by Gunicorn
- **Benefits**: Better performance, process isolation, auto-restart

### 3. **Environment Variables**
- **Development**: Hardcoded values in code
- **Production**: Environment variables for security

### 4. **Logging**
- **Development**: Console output
- **Production**: Structured file logging with rotation

### 5. **Security**
- **Development**: Basic setup
- **Production**: SSL, security headers, firewall

## Migration Checklist

When moving from development to production:

- [ ] Install PostgreSQL 15
- [ ] Install asyncpg: `uv add asyncpg`
- [ ] Update DATABASE_URL in db.py
- [ ] Install Gunicorn: `uv add gunicorn`
- [ ] Create gunicorn.conf.py
- [ ] Create systemd service
- [ ] Set up Nginx (optional)
- [ ] Configure SSL certificates
- [ ] Set up log rotation
- [ ] Create backup scripts
- [ ] Test database migration
- [ ] Verify all endpoints work

## Performance Comparison

| Metric | Development | Production |
|--------|-------------|------------|
| **Concurrent Users** | 1-10 | 1000+ |
| **Database Performance** | Good | Excellent |
| **Memory Usage** | Low | Optimized |
| **Reliability** | Basic | High |
| **Monitoring** | None | Comprehensive | 