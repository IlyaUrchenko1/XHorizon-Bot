FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# System deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python deps first for better caching
COPY app/requirements.txt /app/app/requirements.txt
RUN pip install --upgrade pip \
    && pip install -r /app/app/requirements.txt

# Copy all project (alembic.ini, migrations, app/, common/, settings/, etc.)
COPY . /app

# Entrypoint to optionally run migrations then start API
COPY app/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 8000

# Default to API server; can be overridden in docker-compose
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


