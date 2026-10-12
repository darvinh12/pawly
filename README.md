# Pawly

Repositorio del proyecto **Pawly** (red social de mascotas) de la asignatura
Aplicaciones con Tecnología Internet — UCV.

Contiene el entorno de desarrollo construido en el Laboratorio #9: una aplicación
**Django** con base de datos **SQLite**, desplegada con **Docker Compose** y con el
servidor de aplicación separado del servidor de base de datos.

## Requisitos previos

| Requisito | Versión |
|---|---|
| WSL con Ubuntu | 22.04 LTS |
| Docker Desktop | con integración WSL activada |
| Python | 3.10 |
| Django | 4.2.7 |
| Visual Studio Code | extensiones Python y WSL |

## Estructura del proyecto

```
pawly/
├── .github/
│   ├── actions/docker-repeat/   # Acción propia de GitHub Actions (Docker)
│   └── workflows/               # Workflow de integración continua
├── configPawly/                 # Configuración del proyecto Django
├── PawlyApp/                    # Aplicación: modelos, vistas, rutas, plantillas
├── SecurityApp/                 # Usuarios, roles, permisos, inicio de sesión y auditoría
├── locale/                      # Traducciones de la interfaz (inglés)
├── data/                        # Base de datos SQLite (volumen compartido)
├── Dockerfile                   # Imagen del servidor de aplicación
├── docker-compose.yml           # Orquestación: servidor web + servidor de BD
├── requirements.txt             # Dependencias de Python
└── manage.py
```

## Cómo levantar el entorno con Docker

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
```

La aplicación queda disponible en http://localhost:8000

Para detener los contenedores:

```bash
docker compose down
```

El volumen `bd_data` se conserva entre ejecuciones, por lo que la base de datos no
se pierde al apagar los contenedores.

## Cómo trabajar sin Docker (desarrollo local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Usuarios, roles e idiomas

La aplicación `SecurityApp` reemplaza el usuario de Django por `SecurityApp.User`, que pide un
correo único y permite entrar con el usuario o con el correo.

- **Roles:** son grupos de Django, `Administrator` y `Member`. Se crean solos al ejecutar `migrate`.
  Los usuarios que se registran quedan en `Member`.
- **Permisos propios:** `ban_user` y `moderate_content`, que tiene el rol `Administrator`.
- **Auditoría:** el modelo `AuditLog` guarda los registros, los inicios de sesión (también los
  fallidos) y los cierres de sesión. Se consulta, solo lectura, en `/admin/`.
- **Idiomas:** el español es el idioma principal y el inglés está en `locale/en`. El idioma se
  cambia en Ajustes (botones Español / English), que envían el formulario a `/i18n/setlang/`. Los textos nuevos se marcan con `{% trans %}` en las
  plantillas.
- **Panel de administración:** `/admin-panel/` solo lo abre quien tiene el permiso
  `moderate_content`, es decir, el rol `Administrator`.

## Pantallas

Todas extienden de `base.html`. Las de la aplicación usan además `base_app.html` (barra superior
y menú) y el panel usa `base_admin.html`.

| Ruta | Pantalla | Ruta | Pantalla |
|---|---|---|---|
| `/login/` | Iniciar sesión | `/messages/` | Mensajes |
| `/register/` | Registro, paso 1 | `/messages/1/` | Conversación |
| `/register/profile/` | Registro, paso 2 | `/notifications/` | Notificaciones |
| `/password-reset/` | Recuperar contraseña | `/profile/` | Mi perfil |
| `/` | Inicio | `/profile/settings/` | Ajustes |
| `/search/` | Buscar | `/my-pets/new/` | Nueva mascota |
| `/adoption/` | Feed de adopción | `/my-pets/<id>/` | Perfil de mascota |
| `/adoption/<id>/` | Ficha de la mascota | `/my-pets/<id>/edit/` | Editar mascota |
| `/pets/<id>/apply/` | Postulación | `/users/1/` | Perfil de otro usuario |
| `/admin-panel/` | Panel de administración | `/posts/new/` | Nueva publicación |
| `/messages/<id>/` | Conversación | `/posts/1/` y `/posts/1/report/` | Publicación y reporte |

## Producto mínimo viable (Reto 14)

El MVP es el ciclo de adopción: una persona registra su mascota, la pone en adopción, otra la
encuentra en el feed y se postula, y los dos coordinan por el chat que se abre con la postulación.

| Caso de uso | Dónde |
|---|---|
| UC-05 Editar perfil humano | `/register/profile/`, se ve en `/profile/` |
| UC-06 y UC-07 Crear y editar perfil de mascota | `/my-pets/new/` y `/my-pets/<id>/edit/` |
| UC-16 Marcar y quitar de adopción | Interruptor "Poner en adopción" del formulario de la mascota |
| UC-17 Navegar el feed de adopciones | `/adoption/`, muestra las mascotas en adopción de los demás |
| UC-18 Postularse para adoptar | `/pets/<id>/apply/`, no deja postularse a una mascota propia ni dos veces |
| UC-22, UC-23 y UC-24 Chat | La postulación abre el chat en `/messages/<id>/` |
| UC-31 Gestionar usuarios | `/admin/` y `/admin-panel/` (vetar y quitar el veto) |

Los modelos están en `PawlyApp/models.py` y siguen el modelo de dominio: `Profile`, `Pet`,
`Application`, `Chat` y `Message`. Todos están registrados en el sitio de administración de
Django (`/admin/`). Inicio, búsqueda, notificaciones, publicaciones y el perfil de otro usuario
siguen con datos de ejemplo porque no son parte del MVP.

Para cargar datos de ejemplo (3 usuarios y 8 mascotas en adopción):

```bash
docker compose exec web python manage.py loaddata demo
```

Los usuarios de ejemplo son `luis`, `lunita` y `daniela`, con la contraseña `Pawly-2026`.

Como se cambió el modelo de usuario, la base de datos anterior no sirve. Hay que borrarla y
volver a migrar:

```bash
docker compose down -v
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

## Despliegue en Render (solo repositorio personal)

Esta sección y los archivos `render.yaml`, `deploy/render.Dockerfile`, `deploy/start.sh` y
`.gitattributes` solo existen en el repositorio personal. Sirven para ver la aplicación en
Render y no van en el repositorio del equipo.

Render construye la imagen con `deploy/render.Dockerfile`. Al arrancar, `deploy/start.sh` aplica las
migraciones, carga los datos de ejemplo, crea el administrador y levanta `gunicorn`. `whitenoise`
sirve los archivos estáticos.

| Variable | Para qué sirve |
|---|---|
| `DJANGO_SECRET_KEY` | Clave secreta de Django (Render la genera) |
| `DJANGO_DEBUG` | `False` en Render |
| `DJANGO_SERVE_MEDIA` | `True` para que Django sirva las fotos de `media/` |
| `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD` | Administrador que se crea al arrancar |

En el plan gratuito el servicio se duerme tras 15 minutos sin visitas y la base SQLite vuelve a
empezar en cada despliegue, con los datos de ejemplo cargados de nuevo.

## Arquitectura

El laboratorio plantea separar el servidor de aplicaciones del servidor de base de
datos para mejorar la seguridad de acceso, optimizar el rendimiento y facilitar las
tareas de TI y desarrollo. Este repositorio implementa esa separación con dos
contenedores:

| Contenedor | Imagen | Rol |
|---|---|---|
| `pawly_web` | construida desde el `Dockerfile` | Servidor de aplicación (Django) |
| `pawly_db` | `alpine:3.21` | Servidor de base de datos: administra el volumen `bd_data` |

Ambos comparten el volumen `bd_data`, donde reside el archivo `db.sqlite3`. El
contenedor web no arranca hasta que el contenedor de base de datos pasa su
`healthcheck`.

Para comprobar que la base de datos reside en el servidor de base de datos:

```bash
docker compose exec db ls -l /data
```

## Política de control de versiones

Ver [docs/POLITICA_DE_VERSIONES.md](docs/POLITICA_DE_VERSIONES.md)

| Rama | Propósito |
|---|---|
| `master` | Código probado y listo para producción |
| `release` | Candidatos de versión para certificación |
| `develop` | Integración de las ramas de funcionalidad |
| `feature/*` | Trabajo por funcionalidad o programador |

## Guía de estilo de código

Ver [docs/GUIA_DE_ESTILO.md](docs/GUIA_DE_ESTILO.md)

## Integración continua

El workflow `.github/workflows/action-workflow.yml` se ejecuta en cada `push` e
invoca una acción propia basada en Docker, ubicada en
`.github/actions/docker-repeat`. El resultado se consulta en la pestaña Actions del
repositorio.

## Diferencias respecto al laboratorio

| Punto del laboratorio | Qué se hizo aquí | Motivo |
|---|---|---|
| `docker-compose.yml` con un solo servicio `web` | Dos servicios: `web` y `db` con volumen compartido | Implementar la separación de servidores que describe el propio laboratorio |
| `'NAME': BASE_DIR / 'db.sqlite3'` | `'NAME': BASE_DIR / 'data' / 'db.sqlite3'` | Que la base de datos resida en el volumen compartido |
| `ROM python:3` en el Dockerfile de la acción | `FROM python:3` | Error tipográfico: `ROM` no es una instrucción de Docker |
| `::set-output` para devolver valores | Escritura en `GITHUB_OUTPUT` | GitHub deprecó esa sintaxis |
| `actions/checkout@v1` | `actions/checkout@v4` | La v1 corre sobre una versión de Node retirada de los runners |
| Ubuntu 18.04 en los prerrequisitos | Ubuntu 22.04 LTS | La 18.04 ya no está disponible; las capturas del propio laboratorio son de 22.04 |
| No menciona `.gitignore` ni `.dockerignore` | Se agregaron ambos | Evitar versionar el entorno virtual y reducir el tamaño de la imagen |

## Problemas frecuentes

| Problema | Solución |
|---|---|
| `python3: The term 'python3' is not recognized` | Agregar Python a la ruta del sistema |
| `Python was not found` | Desactivar los alias de ejecución en "Manage App Execution Aliases" |
| `Couldn't import Django` | Activar el entorno virtual con `source .venv/bin/activate` |
| `The command 'docker' could not be found in this WSL 2 distro` | Activar la integración WSL en Docker Desktop |
