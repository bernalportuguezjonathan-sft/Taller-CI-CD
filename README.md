# Taller CI/CD — Despliegue con Docker Compose

Aplicación de tres capas construida y publicada automáticamente en Docker Hub
mediante GitHub Actions, desplegada en producción detrás de Nginx Proxy
Manager con HTTPS (Let's Encrypt) y dominio DuckDNS.

## Servicios

| Servicio | Imagen | Puerto | Descripción |
|---|---|---|---|
| `frontend` | `jonaa07/mi-frontend:latest` | `80` (interno) | Nginx: sirve la página y hace proxy de `/api` hacia el backend |
| `backend` | `jonaa07/mi-api:latest` | `5000` (interno) | Flask: verifica la conexión real contra PostgreSQL |
| `db` | `postgres:16-alpine` | `5432` (interno) | Base de datos |
| `nginx-proxy-manager` | `jc21/nginx-proxy-manager:latest` | `80`, `81`, `443` | Proxy inverso público: enruta el dominio DuckDNS hacia `frontend` y gestiona el certificado SSL |

Ningún servicio de la aplicación publica puertos hacia el host: solo
`nginx-proxy-manager` lo hace, y es quien recibe el tráfico público (80/443)
y expone la administración (81). La app se consulta por el dominio DuckDNS
bajo HTTPS, nunca por IP:puerto directo.

## Integración continua

`.github/workflows/publicar.yml` se ejecuta en cada push a `main`: inicia sesión
en Docker Hub, construye las dos imágenes (`backend` y `frontend`) y las publica
con las etiquetas `latest` y el SHA del commit.

Requiere los secrets `DOCKER_USERNAME` y `DOCKER_TOKEN` en el repositorio
(Settings → Secrets and variables → Actions).

## Despliegue en producción (Oracle Cloud)

En el servidor solo se necesitan `docker-compose.yml` y `.env`, sin código fuente:

```bash
docker compose up -d
```

Variables esperadas en `.env` (ver `.env.example`):

```env
DOCKERHUB_USER=jonaa07
API_TAG=latest
FRONTEND_TAG=latest
POSTGRES_DB=db_principal
POSTGRES_USER=usuario_adso
POSTGRES_PASSWORD=********
```

Pasos para dejarla pública con HTTPS:

1. En Oracle Cloud, habilitar los puertos de entrada 80, 443 y 81.
2. `docker compose up -d` en el servidor.
3. Crear un subdominio en [DuckDNS](https://www.duckdns.org/) apuntando a la IP pública del servidor.
4. Entrar a `http://<ip-publica>:81` (Nginx Proxy Manager), crear un *Proxy Host*
   que redirija el subdominio hacia el contenedor `frontend` (puerto interno `80`).
5. En el mismo Proxy Host, pedir el certificado *Let's Encrypt* y activar *Force SSL*.
