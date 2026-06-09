# Server

FastAPI backend for product-management-ai, managed with [uv](https://docs.astral.sh/uv/).

## Setup

```bash
uv sync
cp .env.example .env
```

## Run

```bash
uv run fastapi dev app/main.py
```

The API runs at http://localhost:8000. Interactive docs at http://localhost:8000/docs.

For production:

```bash
uv run fastapi run app/main.py
```

## Test

```bash
uv run pytest
```

## Layout

```
app/
  main.py            # app factory, middleware, lifespan
  config.py          # settings (pydantic-settings)
  api/routes/        # routers, one module per resource
  schemas/           # pydantic request/response models
  db/
    base.py          # DeclarativeBase for ORM models
    session.py       # async engine, session factory, SessionDep
tests/               # pytest
```

Add a new endpoint by creating a router in `app/api/routes/` and including it in
`app/api/routes/__init__.py`.

## Database (Supabase)

Connection is async SQLAlchemy 2.0 over psycopg 3. Put your Supabase connection
string in `.env` as `DATABASE_URL` (see `.env.example` — the `+psycopg` driver
suffix is required). If you connect through the transaction pooler (port 6543),
also set `DB_USE_POOLER=true` so prepared statements are disabled.

Verify the connection:

```bash
curl http://localhost:8000/health/db   # -> {"status":"ok","database":"connected"}
```

Use the session in any route via the dependency:

```python
from app.db.session import SessionDep

@router.get("/items")
async def list_items(session: SessionDep):
    ...
```

## Migrations (Alembic)

Alembic is configured (async template) to read `DATABASE_URL` from your settings
and autogenerate against `Base.metadata` — no URL lives in `alembic.ini`.

Workflow:

1. Define a model subclassing `app.db.base.Base` under `app/models/`, e.g.
   `app/models/project.py`.
2. Import it in `app/models/__init__.py` so autogenerate can see it.
3. Generate and apply the migration:

```bash
uv run alembic revision --autogenerate -m "add project table"
uv run alembic upgrade head
```

Other useful commands:

```bash
uv run alembic downgrade -1     # roll back one revision
uv run alembic current          # show applied revision
uv run alembic history          # list revisions
```

Run migrations against the **direct** connection (port 5432), not the
transaction pooler — pgbouncer in transaction mode can't run DDL reliably.
