#!/bin/sh

echo "Starting deployment script..."

# Django static fayllarni yig'ish
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Database migratsiyalarini bajarish
echo "Applying database migrations..."
python manage.py migrate

# Superuser yaratish (agar kerak bo'lsa)
DJANGO_SUPERUSER_USERNAME=${DJANGO_SUPERUSER_USERNAME:-admin}
DJANGO_SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-admin@malefashion.uz}
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD:-adminpassword}

echo "Creating superuser if not exists..."
python manage.py createsuperuser \
  --noinput \
  --username $DJANGO_SUPERUSER_USERNAME \
  --email $DJANGO_SUPERUSER_EMAIL || echo "Superuser already exists"

# Gunicorn serverini ishga tushirish
echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
