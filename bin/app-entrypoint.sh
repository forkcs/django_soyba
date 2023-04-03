#!/bin/bash

# Wait for the database to become available
echo "Waiting for database to become available..."
while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done
echo "Database is available."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start the Gunicorn server
echo "Starting Gunicorn server..."
gunicorn myproject.wsgi:application \
  --bind 0.0.0.0:"$APP_PORT" \
  --log-level=info
