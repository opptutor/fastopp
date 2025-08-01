# PostgreSQL Production Installation Guide

This guide covers setting up PostgreSQL with asyncpg for production deployment on DigitalOcean Ubuntu 24.04.

## Overview

- **Development**: SQLite with aiosqlite
- **Production**: PostgreSQL with asyncpg + pgvector (optional)
- **Server**: DigitalOcean Ubuntu 24.04 Droplet
- **Process Manager**: Gunicorn + Uvicorn

## Quick Start (Simplified - No Nginx)

For smaller applications (< 500 concurrent users), you can run FastAPI directly:

### 1. Install Dependencies

```bash
# Add production dependencies
uv add asyncpg gunicorn
```

### 2. Update Database URL

```python
# In db.py
DATABASE_URL = "postgresql+asyncpg://fastopp_user:your_secure_password@localhost/fastopp_db"
```

### 3. Run with Gunicorn

```bash
# Simple production command
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 4. SSL with FastAPI (Optional)

```bash
# Install SSL dependencies
uv add python-multipart

# Run with SSL certificates
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:443 --certfile=/path/to/cert.pem --keyfile=/path/to/key.pem
```

That's it! FastAPI handles everything else.

---

## Full Setup (With Nginx - Optional)

For larger applications or if you want more control:

## 1. Server Setup (DigitalOcean Ubuntu 24.04)

### Initial Server Configuration

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git build-essential python3 python3-pip python3-venv

# Create application user
sudo adduser fastopp
sudo usermod -aG sudo fastopp
```

### Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow OpenSSH
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000  # For development/testing
sudo ufw enable
```

## 2. PostgreSQL Installation

### Install PostgreSQL 15

```bash
# Add PostgreSQL repository
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt update

# Install PostgreSQL
sudo apt install -y postgresql-15 postgresql-contrib-15

# Start and enable PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Configure PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# Create database and user
CREATE DATABASE fastopp_db;
CREATE USER fastopp_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE fastopp_db TO fastopp_user;

# Enable pgvector extension (optional, for AI features)
CREATE EXTENSION IF NOT EXISTS vector;

# Exit PostgreSQL
\q
```

### Configure PostgreSQL for Remote Access

```bash
# Edit PostgreSQL configuration
sudo nano /etc/postgresql/15/main/postgresql.conf

# Add/modify these lines:
listen_addresses = 'localhost'
port = 5432
max_connections = 100
shared_buffers = 256MB
effective_cache_size = 1GB
```

```bash
# Configure client authentication
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Add this line for local connections:
local   fastopp_db    fastopp_user                    md5
```

```bash
# Restart PostgreSQL
sudo systemctl restart postgresql
```

## 3. Application Deployment

### Install Application Dependencies

```bash
# Switch to application user
sudo su - fastopp

# Clone application
git clone https://github.com/your-repo/fastopp.git
cd fastopp

# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.cargo/env

# Install Python dependencies
uv sync
```

### Update Database Configuration

```bash
# Edit db.py for production
nano db.py
```

Update the `DATABASE_URL`:

```python
# Production database URL
DATABASE_URL = "postgresql+asyncpg://fastopp_user:your_secure_password@localhost/fastopp_db"

# For pgvector support (optional)
# DATABASE_URL = "postgresql+asyncpg://fastopp_user:your_secure_password@localhost/fastopp_db"
```

### Install Production Dependencies

```bash
# Add production dependencies
uv add asyncpg gunicorn
```

Update `pyproject.toml`:

```toml
[project]
dependencies = [
    # ... existing dependencies ...
    "asyncpg>=0.29.0",
    "gunicorn>=21.2.0",
]
```

## 4. Gunicorn + Uvicorn Configuration

### Create Gunicorn Configuration

```bash
# Create gunicorn config
nano gunicorn.conf.py
```

```python
# gunicorn.conf.py
import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/fastopp/access.log"
errorlog = "/var/log/fastopp/error.log"
loglevel = "info"

# Process naming
proc_name = "fastopp"

# Server mechanics
daemon = False
pidfile = "/var/run/fastopp/gunicorn.pid"
user = "fastopp"
group = "fastopp"
tmp_upload_dir = None

# SSL (if using HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"
```

### Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/fastopp.service
```

```ini
[Unit]
Description=FastOpp Gunicorn daemon
After=network.target

[Service]
User=fastopp
Group=fastopp
WorkingDirectory=/home/fastopp/fastopp
Environment="PATH=/home/fastopp/.cargo/bin:/home/fastopp/.local/bin"
ExecStart=/home/fastopp/.cargo/bin/uv run gunicorn main:app -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### Create Log Directory

```bash
# Create log directory
sudo mkdir -p /var/log/fastopp
sudo chown fastopp:fastopp /var/log/fastopp

# Create run directory
sudo mkdir -p /var/run/fastopp
sudo chown fastopp:fastopp /var/run/fastopp
```

## 5. Nginx Configuration (Optional - Skip for < 100 Users)

**Note**: Nginx is only needed for applications with 100+ concurrent users. For smaller applications, FastAPI + Gunicorn can serve directly without Nginx.

### When to Use Nginx

- ✅ **100+ concurrent users**
- ✅ **Need load balancing**
- ✅ **Want advanced caching**
- ✅ **Complex SSL requirements**

### When to Skip Nginx

- ✅ **< 100 concurrent users** (your use case)
- ✅ **Simple setup preferred**
- ✅ **FastAPI handles everything you need**

### Install Nginx (Only if needed)

```bash
sudo apt install -y nginx
```

### Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/fastopp
```

```nginx
server {
    listen 80;
    server_name your-domain.com;  # Replace with your domain

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # Proxy to Gunicorn
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    # Static files (if any)
    location /static/ {
        alias /home/fastopp/fastopp/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### Enable Nginx Site

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/fastopp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 6. SSL Certificate (Let's Encrypt)

### Option A: SSL with FastAPI (Recommended for < 100 Users)

FastAPI can handle SSL directly without Nginx:

```bash
# Install SSL dependencies
sudo apt install -y certbot

# Obtain SSL certificate
sudo certbot certonly --standalone -d your-domain.com

# Run with SSL certificates
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:443 \
  --certfile=/etc/letsencrypt/live/your-domain.com/fullchain.pem \
  --keyfile=/etc/letsencrypt/live/your-domain.com/privkey.pem
```

### Custom Domain Configuration with Gunicorn

Unlike Nginx, Gunicorn doesn't have a configuration file for multiple domains. Instead, you handle domain routing in your FastAPI application:

#### Method 1: Environment Variables (Recommended)

```bash
# Set your domain in environment
export DOMAIN_NAME="your-domain.com"
export DOMAIN_PORT="443"

# Run with environment variables
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:${DOMAIN_PORT} \
  --certfile=/etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem \
  --keyfile=/etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem
```

#### Method 2: Gunicorn Configuration File

Create `gunicorn.conf.py`:

```python
# gunicorn.conf.py
import os
import multiprocessing

# Domain configuration
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "your-domain.com")
DOMAIN_PORT = os.getenv("DOMAIN_PORT", "443")

# Server socket
bind = f"0.0.0.0:{DOMAIN_PORT}"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50

# SSL configuration (if using HTTPS)
if DOMAIN_PORT == "443":
    certfile = f"/etc/letsencrypt/live/{DOMAIN_NAME}/fullchain.pem"
    keyfile = f"/etc/letsencrypt/live/{DOMAIN_NAME}/privkey.pem"

# Logging
accesslog = "/var/log/fastopp/access.log"
errorlog = "/var/log/fastopp/error.log"
loglevel = "info"

# Process naming
proc_name = "fastopp"

# Server mechanics
daemon = False
pidfile = "/var/run/fastopp/gunicorn.pid"
user = "fastopp"
group = "fastopp"
tmp_upload_dir = None
```

Run with config file:

```bash
# Set environment variables
export DOMAIN_NAME="your-domain.com"
export DOMAIN_PORT="443"

# Run with configuration file
uv run gunicorn main:app -c gunicorn.conf.py
```

#### Method 3: Multiple Domains in FastAPI

If you need to serve multiple domains from the same application:

```python
# main.py
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.middleware("http")
async def domain_middleware(request: Request, call_next):
    """Handle multiple domains"""
    host = request.headers.get("host", "")
    
    # Redirect www to non-www
    if host.startswith("www."):
        new_host = host.replace("www.", "", 1)
        return RedirectResponse(
            url=f"https://{new_host}{request.url.path}",
            status_code=301
        )
    
    # Handle different domains
    if host == "api.your-domain.com":
        # API-specific logic
        pass
    elif host == "admin.your-domain.com":
        # Admin-specific logic
        pass
    
    response = await call_next(request)
    return response

@app.get("/")
async def root(request: Request):
    host = request.headers.get("host", "")
    return {"message": f"Hello from {host}"}
```

#### Method 4: Systemd Service with Environment

Create `/etc/systemd/system/fastopp.service`:

```ini
[Unit]
Description=FastOpp Gunicorn daemon
After=network.target

[Service]
User=fastopp
Group=fastopp
WorkingDirectory=/home/fastopp/fastopp
Environment="PATH=/home/fastopp/.cargo/bin:/home/fastopp/.local/bin"
Environment="DOMAIN_NAME=your-domain.com"
Environment="DOMAIN_PORT=443"
ExecStart=/home/fastopp/.cargo/bin/uv run gunicorn main:app -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### DNS Configuration

Unlike Nginx, you don't need server blocks. Instead, configure your DNS:

#### 1. Point Domain to Server

In your domain registrar's DNS settings:

```text
Type    Name    Value
A       @       YOUR_SERVER_IP
A       www     YOUR_SERVER_IP
```

#### 2. Test Domain Resolution

```bash
# Test DNS propagation
nslookup your-domain.com
dig your-domain.com

# Test from server
curl -H "Host: your-domain.com" http://localhost:8000/
```

#### 3. Verify SSL Certificate

```bash
# Test SSL certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com
```

### Option B: SSL with Nginx (For 100+ Users)

```bash
# Install Certbot with Nginx
sudo apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

## 7. Database Migration

### Initialize Production Database

```bash
# Switch to application user
sudo su - fastopp
cd fastopp

# Initialize database
uv run python oppman.py init
```

### Environment Variables (Recommended)

```bash
# Create environment file
nano .env
```

```bash
# .env
DATABASE_URL=postgresql+asyncpg://fastopp_user:your_secure_password@localhost/fastopp_db
SECRET_KEY=your_very_secure_secret_key_here
```

Update `db.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
```

## 8. Start Services

### Enable and Start Services

```bash
# Enable and start FastOpp service
sudo systemctl enable fastopp
sudo systemctl start fastopp

# Check status
sudo systemctl status fastopp
```

### Verify Installation

```bash
# Check if service is running
curl http://localhost:8000/

# Check logs
sudo journalctl -u fastopp -f
```

## 9. Monitoring and Maintenance

### Log Rotation

```bash
sudo nano /etc/logrotate.d/fastopp
```

```text
/var/log/fastopp/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 fastopp fastopp
    postrotate
        systemctl reload fastopp
    endscript
}
```

### Backup Script

```bash
nano backup.sh
```

```bash
#!/bin/bash
# Database backup script
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/fastopp/backups"
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -h localhost -U fastopp_user fastopp_db > $BACKUP_DIR/fastopp_db_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/fastopp_db_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "*.sql.gz" -mtime +7 -delete
```

```bash
chmod +x backup.sh
```

## 10. Troubleshooting

### Common Issues

1. **Database Connection Error**

   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Test connection
   psql -h localhost -U fastopp_user -d fastopp_db
   ```

2. **Permission Issues**

   ```bash
   # Fix log directory permissions
   sudo chown -R fastopp:fastopp /var/log/fastopp
   sudo chown -R fastopp:fastopp /var/run/fastopp
   ```

3. **Service Won't Start**

   ```bash
   # Check service logs
   sudo journalctl -u fastopp -n 50
   
   # Test manually
   sudo su - fastopp
   cd fastopp
   uv run gunicorn main:app -c gunicorn.conf.py
   ```

## Summary

### For < 100 Concurrent Users (Recommended)

- ✅ **PostgreSQL 15** with asyncpg driver
- ✅ **Gunicorn + Uvicorn** for production serving
- ✅ **FastAPI handles SSL** directly (no Nginx needed)
- ✅ **Systemd service** for process management
- ✅ **Log rotation** and monitoring
- ✅ **Database backups** automation

### For 100+ Concurrent Users

- ✅ **PostgreSQL 15** with asyncpg driver
- ✅ **Gunicorn + Uvicorn** for production serving
- ✅ **Nginx** reverse proxy (optional)
- ✅ **SSL certificates** with Let's Encrypt
- ✅ **Systemd service** for process management
- ✅ **Log rotation** and monitoring
- ✅ **Database backups** automation

Your FastAPI application is now production-ready with async PostgreSQL support!
