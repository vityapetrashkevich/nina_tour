  #!/bin/sh

echo "Waiting for Postgres..."
while ! nc -z database 5432; do
  sleep 1
done
echo "Postgres is up."

echo "Running migrations..."
alembic upgrade head

echo "Starting backend..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
