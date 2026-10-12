#!/bin/sh
# Arranque en Render: crea las tablas y los roles, crea el administrador y levanta gunicorn.
# El plan gratuito no guarda archivos entre despliegues, así que la base SQLite empieza vacía cada vez.
set -e
python manage.py migrate --noinput

# Usa DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL y DJANGO_SUPERUSER_PASSWORD; si ya existe, sigue
python manage.py createsuperuser --noinput || true

exec gunicorn configPawly.wsgi --bind "0.0.0.0:${PORT:-8000}" --workers 2
