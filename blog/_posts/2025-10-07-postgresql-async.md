---
layout: post
title: "Architectural Consistency When Working with a PostgreSQL Async Database"
date: 2025-10-07
author: Craig Oda
author_bio: "Craig Oda is a partner at Oppkey and an active contributor to FastOpp"
image: /assets/images/workshop.webp
excerpt: "How I learned that async databases need async migrations, and why the 'quick fix' approach doesn't scale"
---

## PostgreSQL Failing with Async in Production Although SQLite Works on my Mac

Last week, I was working on our FastOpp project and ran into a classic developer problem: "It works on my machine, but not in production." Specifically, our FastAPI application worked perfectly with SQLite during development, but when I tried to switch to PostgreSQL in production on Leapcell using the Leapcell PostgreSQL service,
database access broke.

## Converting Database Connection to Sync Led to More Problems

My first instinct was the same as many developers: find a workaround. I discovered that our
migration tool (Alembic) was trying to use synchronous database operations while our
FastAPI app was using asynchronous ones.

The "solution" I found online was to convert the database URL from async to sync during migrations:

```python
# The "quick fix" approach - BEFORE
def run_migrations_online() -> None:
    database_url = os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))
    
    # Convert async URLs to regular URLs for migrations
    if database_url and "aiosqlite" in database_url:
        database_url = database_url.replace("sqlite+aiosqlite://", "sqlite://")
    elif database_url and "asyncpg" in database_url:
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    
    connectable = engine_from_config(...)  # SYNC engine
    with connectable.connect() as connection:  # SYNC connection
        context.configure(connection=connection, ...)
```

I committed the solution after only testing it on SQLite locally and unfortunately forgot
to test it on PostgreSQL.  Several months passed and my laziness came back to bite
me and cost me many hours. As I am new to Alembic, I didn't know there was an
async Alembic version and the logic of using synchronous calls for migrations seemed fine
to me as migrations _felt_ synchronous.

## The Real Problem: Architectural Mismatch

Here's what I learned: when you build an async application, try to keep as much of your code
as possible async. Although it is possible to "convert" async to sync in the middle of your stack,
it may cause problems in the future when you have to maintain your own code.

The issue wasn't with the database or the migration tool. The issue was that I was trying to mix two different paradigms:

- **My FastAPI app**: Async throughout (using `asyncpg` for PostgreSQL)
- **My migrations**: Sync operations (using sync database drivers)

## The Right Solution: Go All-In on Async

Instead of trying to convert between async and sync, I updated our migration system to be async from the ground up. Here's the transformation:

## The Solution: Pure Async Approach

```python
# The RIGHT approach - AFTER
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(...)  # ASYNC engine
    async with connectable.connect() as connection:  # ASYNC connection
        await connection.run_sync(do_run_migrations)  # Magic happens here!
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())
```

The key insight was this line:

```python
await connection.run_sync(do_run_migrations)
```

This allows you to run synchronous migration code within an async database connection.

## The Results: What Actually Happened

After implementing the async approach, here's what we achieved:

### **Single Driver Architecture**

- **Before**: Needed both `asyncpg` (app) + `psycopg2` (migrations)
- **After**: Only `asyncpg` for everything - no driver conflicts

### **Consistent Database URLs**

- **Before**: App used `postgresql+asyncpg://` but migrations converted to `postgresql://`
- **After**: Both use `postgresql+asyncpg://` - same driver throughout

### **Works with Both Databases**

```bash
# SQLite (development)
export DATABASE_URL="sqlite+aiosqlite:///./test.db"
uv run alembic upgrade head  # ✅ Works

# PostgreSQL (production)  
export DATABASE_URL="postgresql+asyncpg://user@localhost:5432/fastopp"
uv run alembic upgrade head  # ✅ Works
```

## Why This Matters for Students

If you're learning web development, here's the takeaway: **consistency is more important than clever workarounds**. 

When you're building modern web applications:

- Choose your architecture (sync or async) and stick with it
- Don't try to mix paradigms just because it seems easier
- The "quick fix" often becomes the "long-term problem"

## Async Database Access May Not Be Justified

Standardizing on synchronous database access for everything is simpler and will
work for most apps.  Asynchronous operations are needed only for heavy
SQL joins where the response takes many seconds or minutes and need to be run
in real-time.  In most cases, people will run the operation in the background
with Celery.  

However, even if I don't see the need for asynchronous database connections,
other people might.  FastOpp is a learning tool and I want to provide
asynchronous connectivity to support the creativity of others.

## The Business Lesson

As a manager, I've seen this pattern play out in many projects. The "quick fix"
that saves 30 minutes today often costs hours or days later. In this case, spending the extra time to properly implement async migrations saved us from a maintenance nightmare. The "quick fix"
was also forgotten because there is no real-world impact in using synchronous migrations.

The modern approach - using async patterns throughout - is not just technically correct, it's also more maintainable and scalable.

## What's Next

Our FastOpp project now supports both SQLite (for development) and PostgreSQL (for production) with a single, consistent async architecture. No more driver conflicts, no more sync/async mixing, and no more "it works on my machine" problems.

It appears that psycopg3, called psycopg, supports both async and sync. I don't think it's as popular
as asyncpg.  However, I hope to try it out next.
