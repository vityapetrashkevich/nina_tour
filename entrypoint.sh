#!/bin/sh

echo "Waiting for Postgres..."

echo "Postgres is up."

echo "Running migrations..."
alembic upgrade head

echo "Starting backend..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
