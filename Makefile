# product-management-ai — dev task runner
#
#   make server     run the FastAPI server (server/, port 8000)
#   make client    run the Next.js client (client/, port 3000)
#   make dev         run both together (Ctrl-C stops both)
#   make install     install dependencies for both
#
# client lives in client/ (npm), server in server/ (uv).

.PHONY: server client dev install install-server install-client

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
