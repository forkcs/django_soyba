#!/bin/sh

set -o errexit

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate

echo "Starting Gunicorn server..."
python -m gunicorn config.wsgi:application \
  --bind 0.0.0.0:"$APP_PORT" \
  --log-level=info
