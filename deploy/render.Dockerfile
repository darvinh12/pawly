# Imagen para el despliegue de demostración en Render.
# El Dockerfile de la raíz sigue siendo el del entorno de desarrollo del equipo.
FROM python:3.12.4
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p data && python manage.py collectstatic --noinput
CMD ["sh", "deploy/start.sh"]
