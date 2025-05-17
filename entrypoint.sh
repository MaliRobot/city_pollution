#!/bin/sh

echo "Waiting for Postgres server..."

until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
  echo "Postgres server not available yet - sleeping"
  sleep 5
done

echo "Postgres server is available, checking database..."

# Wait for the actual DB to be available
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q' 2>/dev/null; do
  echo "Database $POSTGRES_DB is not ready yet - sleeping"
  sleep 5
done

echo "Database $POSTGRES_DB is ready - running migrations"

alembic upgrade head

uvicorn city_pollution.main:app --host 0.0.0.0 --port 8000 --reload
