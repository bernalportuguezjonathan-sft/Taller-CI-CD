# Taller CI/CD — Despliegue con Docker Compose

Aplicación de tres capas construida y publicada automáticamente en Docker Hub
mediante GitHub Actions.

## Servicios

| Servicio | Imagen | Puerto | Descripción |
|---|---|---|---|
| `frontend` | `jonaa07/mi-frontend:latest` | `80` | Nginx: sirve la página y hace proxy de `/api` hacia la API |
| `api` | `jonaa07/mi-api:latest` | `5000` (interno) | Flask: verifica la conexión real contra PostgreSQL |
| `db` | `postgres:16-alpine` | `5432` (interno) | Base de datos |

Solo el frontend publica puerto hacia el host, por lo que la aplicación se
consulta en `http://localhost` sin indicar puerto.

## Integración continua

`.github/workflows/publicar.yml` se ejecuta en cada push a `main`: inicia sesión
en Docker Hub, construye las dos imágenes y las publica con las etiquetas
`latest` y el SHA del commit.

Requiere los secrets `DOCKER_HUB_USERNAME` y `DOCKER_HUB_TOKEN` en el repositorio.

## Despliegue

En el servidor solo se necesitan `docker-compose.yml` y `.env`, sin código fuente:

```bash
docker compose up -d
```

Variables esperadas en `.env`:

```env
DOCKERHUB_USER=jonaa07
API_TAG=latest
FRONTEND_TAG=latest
FRONTEND_PORT=80
POSTGRES_DB=db_principal
POSTGRES_USER=usuario_adso
POSTGRES_PASSWORD=********
```
