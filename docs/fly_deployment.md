# Fly Deployment

Your FastOpp program wants to fly! 

## Overview 

FastOpp provides an opinionated framework for FastAPI with the following features:

* Admin panel similar to Django 
* A Python program to work with the database
* Admin panel example with custom styling
* Django-style HTML templates with modern UI components
* Replaceable style templates to get started
* API endpoints to connect to other frontend frameworks
* Auto-generated documentation for API endpoints

 You can deploy it yourself. It needs to be able to run uvicorn and mount a persistent volume for a single SQLite file. 
 
 It does not use PostgreSQL or Nginx.

It uses Fly.io, since it's cheap, repeatable, and volume-backed. Run uvicorn directly. Store SQLite at /data/app.db.

## Pricing

This deployment is intended to be low-cost. You will be using the "Pay As You Go Plan." 

You will need to log in and add a payment method.

> "To start deploying apps you'll need to add a payment method"
> 
> Great for side projects, test environments, or projects with a small team. Run basic full-stack apps close to your users, paying only for what you use.
> 
> Deploy in 30+ regions
> 
> No minimum spend commitment

## Let's Get Started!

### 0) Prereqs

- **macOS** with **Homebrew** installed
- **Your FastAPI (FastOpp) repo** cloned locally

```bash
brew install flyctl
fly auth signup   # or: fly auth login
```
Opens up a webpage on fly.io. You can use Google or GitHub to create an account.

> "Your flyctl should be connected now. Feel free to close this tab"

### 1) Add deploy files to the repo

Add a `Dockerfile` to the project root:

```Dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_SYSTEM_PYTHON=1 \
    PORT=8000

RUN apt-get update && apt-get install -y --no-install-recommends curl build-essential \
  && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen --no-dev

COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Add a `.dockerignore`:

```gitignore
.git
.venv
__pycache__/
*.db
```

### 2) Initialize fly app (nor deployed yet)

```bash
fly launch --no-deploy
# Answer:
# - App name: <enter> or custom
# - Region: choose one near you
# - Use Postgres: No
# - Create a Dockerfile: No (you already added one)
```

You should see something like this:

```bash
jcasman@MacBook-Air-6 fastcfv % fly launch --no-deploy
Scanning source code
Detected a Dockerfile app
Creating app in /Users/jcasman/Development/fastcfv
We're about to launch your app on Fly.io. Here's what you're getting:

Organization: Jesse Casman (fly launch defaults to the personal org)
Name: fastcfv (derived from your directory name)
Region: San Jose, California (US) (this is the fastest region for you)
App Machines: shared-cpu-1x, 1GB RAM (most apps need about 1GB of RAM)
Postgres: (not requested)
Redis: (not requested)
Tigris: (not requested)
```

### 3) Create and mount a persistent volume

Note: Pick the same region you chose above. However, just use its short code, not the full name. For example, it's not "San Jose, California (US)", it's "sjc" - You can find your region code using:

```bash
flyctl platform regions
```

Now run:

```bash
fly volumes create data --region <REGION> --size 1
```

Note: If you get this error, you can ignore.

```text
Warning! Every volume is pinned to a specific physical host. You should create two or more volumes per application to avoid downtime. 
```

### 4) Edit fly.toml

Open the generated `fly.toml`. Ensure these blocks exist:

You probably have this:

```toml
app = "<your-app-name>"
primary_region = '<your-region>'

[build]

[http_service]
internal_port = 8000
force_https = true
auto_stop_machines = 'stop'
auto_start_machines = true
min_machines_running = 0
processes = ['app']

[[vm]]
memory = '1gb'
cpu_kind = 'shared'
cpus = 1
```

Make sure this is included, too.

```toml
[env]
  ENVIRONMENT = "production"

[[mounts]]
  source = "data"
  destination = "/data"

[[services]]
  internal_port = 8000
  protocol = "tcp"
  [[services.ports]]
    port = 80
    handlers = ["http"]
  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

### 5) Set secrets and DB URL

```bash
fly secrets set SECRET_KEY=$(openssl rand -hex 32)
fly secrets set DATABASE_URL="sqlite+aiosqlite:////data/app.db"
```

### 6) Single-machine only (SQLite requires one writer)

```bash
fly scale count 1
```

Note: If you get this error, do step 7 first

```text
jcasman@MacBook-Air-6 fastcfv % fly scale count 1
Error: failed to grab app config from existing machines, error: could not create a fly.toml from any machines :-(
No machines configured for this app
```

### 7) Deploy

```bash
fly deploy
fly status
fly logs --since 5m
```

### 8) Issue an SSH certificate
You'll be sending SSH commands to fly.io. 

```bash
fly ssh issue --agent
# or: fly ssh issue
```

### 9) Setup up your database using oppman.py

```bash
# upgrade schema
fly ssh console -C "uv run python oppman.py db"
```

_Note, as of Aug 12, 2025, 2pm PT: Jesse has not used the steps below here._

### Back up your database

```bash
fly ssh console -C 'mkdir -p /data/backups && cp /data/app.db /data/backups/app-$(date +%F-%H%M%S).db && ls -lh /data/backups'
```

### Verify persistence

Create a probe row, restart, then read it again.

```bash
# write probe
fly ssh console -C 'uv run python - <<PY
import asyncio, os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
async def main():
    eng = create_async_engine(os.environ["DATABASE_URL"], future=True)
    async with eng.begin() as c:
        await c.execute(text("CREATE TABLE IF NOT EXISTS _probe(k TEXT PRIMARY KEY, v TEXT)"))
        await c.execute(text("INSERT OR REPLACE INTO _probe(k,v) VALUES (\"ping\",\"pong\")"))
    await eng.dispose()
asyncio.run(main())
print("ok")
PY'

# restart
fly apps restart

# read probe
fly ssh console -C 'uv run python - <<PY
import asyncio, os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
async def main():
    eng = create_async_engine(os.environ["DATABASE_URL"], future=True)
    async with eng.connect() as c:
        r = await c.execute(text("SELECT v FROM _probe WHERE k=\"ping\""))
        print(list(r))
    await eng.dispose()
asyncio.run(main())
PY'
# expect: [('pong',)]
```

## Extra Information

### Can fly.io handle persistent storage?

Fly.io Machines provide ephemeral compute, meaning your data is lost when the machine restarts. Fly Volumes offer persistent storage by attaching a slice of an NVMe drive to a machine. This allows you to mount a volume to a specific path on your machine, enabling data persistence across restarts and deployments.

Here's a breakdown:

Fly Machines:
Fly Machines are virtual machines that run your application code. They are designed to be lightweight and scalable, but their storage is ephemeral.

Fly Volumes:
Fly Volumes are persistent storage volumes that can be attached to Fly Machines. They are like physical disks, providing a place to store data that persists even when the machine restarts.

Mounting:
When you mount a volume, you specify a path on the machine's file system where the volume's contents will be accessible.

Use Cases:
Fly Volumes are useful for storing application data that needs to persist, such as user data, configuration files, or databases.

In essence, Fly.io Machines + Mounted Volume provides a way to combine the scalability and speed of Fly Machines with the persistent storage of Fly Volumes, allowing you to build robust and scalable applications that can handle data persistence.

## What is a Dockerfile?

A Dockerfile is essentially a blueprint for building a Docker image. It's a plain text file containing a set of instructions that Docker executes in sequential order to create an image.

A Dockerfile is a simple, plain text file. You create and edit it using any text editor you prefer (like VS Code, Notepad, or even a basic text editor in your terminal like vi or nano).

Key points about creating a Dockerfile

* Plain Text File: It's a regular text file.
* No File Extension (by convention): It's usually named "Dockerfile" (with a capital "D") and has no file extension
* Contains Instructions: The Dockerfile contains a series of commands that Docker executes in order to build the image. These instructions tell Docker things like:
  * What base image to start with (FROM)
  * What files to copy into the image (COPY)
  * What commands to run during the build process (RUN)
  * The default command to execute when a container is launched from the image (CMD)