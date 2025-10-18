#!/usr/bin/env bash
set -euo pipefail

echo "[entrypoint] Waiting for database..."
python - <<'PY'
import asyncio, sys
import asyncpg
import os

uri = os.getenv('SQLALCHEMY_DATABASE_URI') or os.getenv('DATABASE_URL')
if not uri:
    # fallback to settings default to avoid hard fail in local
    uri = 'postgresql+asyncpg://postgres:postgres@db:5432/xhorizon'

uri = uri.replace('postgresql+asyncpg://', 'postgres://')

async def ping():
    for _ in range(60):
        try:
            conn = await asyncpg.connect(uri)
            await conn.close()
            sys.exit(0)
        except Exception:
            await asyncio.sleep(1)
    sys.exit(1)

asyncio.run(ping())
PY

echo "[entrypoint] Running migrations..."
# Autogenerate initial migration if no revision .py files exist
REV_COUNT=$(ls -1 migrations/versions/*.py 2>/dev/null | wc -l | tr -d ' ')
if [ "$REV_COUNT" = "0" ]; then
  echo "[entrypoint] No Alembic .py revisions found. Autogenerating initial migration..."
  alembic revision --autogenerate -m "init" || { echo "[entrypoint] Alembic autogenerate failed"; exit 1; }
else
  echo "[entrypoint] Found $REV_COUNT Alembic revision file(s). Skipping autogenerate."
fi

alembic upgrade head || { echo "[entrypoint] Alembic upgrade failed"; exit 1; }

echo "[entrypoint] Starting: $@"
exec "$@"


