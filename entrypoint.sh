#!/bin/sh
until nc -z -v -w30 $POSTGRES_HOST $POSTGRES_PORT
do
  echo "Waiting for database connection..."
  # wait for 5 seconds before check again
  sleep 5
done

# Once PostgreSQL is available, continue with the script
>&2 echo "Postgres is up - continuing"


alembic upgrade head

uvicorn data_project.main:app --host 0.0.0.0 --port 8000 --reload
