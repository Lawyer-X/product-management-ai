# product-management-ai — dev task runner
#
#   make server     run the FastAPI server (server/, port 8000)
#   make client    run the Next.js client (client/, port 3000)
#   make dev         run both together (Ctrl-C stops both)
#   make install     install dependencies for both
#
#   make migrate m="add foo"   autogenerate a new migration from the models
#   make upgrade               apply all pending migrations (alembic upgrade head)
#   make downgrade             roll back one migration (alembic downgrade -1)
#   make migration-current     show the DB's current revision
#   make migration-history     show the migration history
#   make db-reset              downgrade to base, then re-apply everything
#
# client lives in client/ (npm), server in server/ (uv).

.PHONY: server client dev install install-server install-client \
        migrate upgrade downgrade migration-current migration-history db-reset

# --- server (FastAPI + uv) ---
server:
	cd server && uv run fastapi dev app/main.py

# --- client (Next.js + npm) ---
client:
	cd client && npm run dev

# --- Both at once: start server in the background, client in the
#     foreground, and tear down the server when you Ctrl-C out. ---
dev:
	@echo "Starting server (:8000) and client (:3000) — Ctrl-C to stop both"
	@trap 'kill 0' INT TERM EXIT; \
	( cd server && uv run fastapi dev app/main.py ) & \
	( cd client && npm run dev ) & \
	wait

# --- Dependency install ---
install: install-server install-client

install-server:
	cd server && uv sync

install-client:
	cd client && npm install

# --- Database migrations (Alembic, run from server/) ---

# Autogenerate a migration from the current models. Requires a message:
#   make migrate m="add tickets table"
migrate:
	@test -n "$(m)" || { echo 'Usage: make migrate m="your message"'; exit 1; }
	cd server && uv run alembic revision --autogenerate -m "$(m)"

# Apply all pending migrations.
upgrade:
	cd server && uv run alembic upgrade head

# Roll back the most recent migration.
downgrade:
	cd server && uv run alembic downgrade -1

# Show the revision the database is currently at.
migration-current:
	cd server && uv run alembic current

# Show the full migration history.
migration-history:
	cd server && uv run alembic history --verbose

# Roll the schema all the way back to empty, then re-apply every migration.
# Destructive: drops data in migration-managed tables.
db-reset:
	cd server && uv run alembic downgrade base && uv run alembic upgrade head
