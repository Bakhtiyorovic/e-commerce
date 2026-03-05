#!/bin/sh
set -e

echo "Waiting for database..."
until pg_isready -h db -p 5432; do
  sleep 2
done
echo "Database ready!"

echo "Apply migrations..."
python manage.py migrate

if [ "$DEBUG" != "True" ]; then
  echo "Collect static..."
  python manage.py collectstatic --noinput
fi

echo "Starting app..."
exec "$@"
