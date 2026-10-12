#!/bin/sh
# Solo para el repositorio personal (Render)
# La base de datos empieza vacía en cada despliegue, por eso se migra y se cargan los datos de ejemplo
set -e
python manage.py migrate --noinput
python manage.py loaddata demo

# Crea el administrador con las variables DJANGO_SUPERUSER del servicio
python manage.py createsuperuser --noinput || true

exec gunicorn configPawly.wsgi --bind "0.0.0.0:${PORT:-8000}" --workers 2
