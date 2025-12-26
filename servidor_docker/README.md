Microservicio: proyecto_api (despliegue local)

Este directorio contiene los artefactos para ejecutar el "microservicio" de la API en Docker para desarrollo local.

Archivos clave:
- `Dockerfile` — imagen que instala dependencias y arranca Gunicorn.
- `wsgi.py` — entrypoint WSGI que expone `app` para Gunicorn.
- `traefik_dynamic.yml` — router dinámico de Traefik usado en desarrollo (montado por docker-compose).
- `docker-compose.traefik.yml` — compose local que levanta Traefik + este servicio.

Comandos de uso (desde la raíz del repo):

# Construir y levantar
docker compose -f .\servidor_docker\docker-compose.traefik.yml up --build -d

# Logs
docker compose -f .\servidor_docker\docker-compose.traefik.yml logs -f proyecto_api

Notas:
- En desarrollo montamos un archivo dinámico para Traefik porque en Windows el provider.docker puede no detectar contenedores correctamente.
- La API también escucha directamente en el puerto 5000 (mapeado en el compose) para pruebas rápidas.
- Para producción recomendamos usar una configuración de Traefik que no exponga el dashboard, y separar variables sensibles en un `.env` o en el orquestador.
