## Handoff: Instrucciones para continuar el trabajo (rama: pruebas)

Este documento contiene los pasos ordenados y los comandos necesarios para que tu compañero pueda levantar el proyecto, inicializar la base de datos, ejecutar tests y seguir con las tareas prioritarias (migraciones, CI, DB persistente). Todo en PowerShell (Windows).

---

### 1) Preparación: revisar la rama

1. Clonar el repo o traer la rama `pruebas` y situarse en la raíz del proyecto (la carpeta que contiene `servidor_docker`).
2. Confirmar que los archivos importantes que vienen en la rama están presentes:
   - `servidor_docker/` (Dockerfile, `wsgi.py`, `app.py`, `init_db.py`, `docker-compose.traefik.yml`, `traefik_dynamic.yml`, `README.md`)
   - `app/` (factory, `db`, `ma`, servicios, repositorios, schemas)
   - `test/` (pruebas añadidas, ej. `test_facultad_pagination.py`)
   - `scripts/cleanup-legacy.ps1` (script para archivar la carpeta legacy)

---

### 2) Levantar el entorno con Docker + Traefik (dev)

Desde la raíz del repo (el mismo nivel que `servidor_docker`):

```powershell
# Construir y arrancar Traefik + API en segundo plano
docker compose -f .\servidor_docker\docker-compose.traefik.yml up --build -d

# Ver logs del servicio API (reemplazar nombre si lo cambien)
docker compose -f .\servidor_docker\docker-compose.traefik.yml logs -f proyecto_api
```

Comprobar que los contenedores estén RUNNING:

```powershell
docker ps
```

Verificar Traefik: la configuración file-provider añadida debería registrar un router llamado `proyecto_api_router@file`.

---

### 3) Inicializar la base de datos (única vez)

IMPORTANTE: para evitar condiciones de carrera con Gunicorn no ejecutar `db.create_all()` en import time. El repositorio trae `servidor_docker/init_db.py` para crear las tablas una vez.

Ejecutar dentro del contexto de Docker:

```powershell
docker compose -f .\servidor_docker\docker-compose.traefik.yml run --rm proyecto_api python -m servidor_docker.init_db
```

Salida esperada: mensajes indicando que las tablas fueron creadas / confirmación. Si usan migraciones (Flask-Migrate) reemplazar este paso por `flask db upgrade`.

---

### 4) Probar endpoints y autenticación básica

Endpoints a probar:
- `http://127.0.0.1:5000/test` (requiere Basic Auth)
- `http://127.0.0.1:5000/api/facultades` (soporta `page`, `per_page`, `q`)

Credenciales de ejemplo (fijas en `servidor_docker/app.py` para dev):
- usuario: `amigo1` contraseña: `clave1` (y `amigo2..amigo6` con `clave2..clave6`)

Ejemplo con curl (Windows PowerShell):

```powershell
# GET /test
curl -u amigo1:clave1 http://127.0.0.1:5000/test

# GET /api/facultades
curl -u amigo1:clave1 "http://127.0.0.1:5000/api/facultades?page=1&per_page=5&q=Universidad"
```

Si queréis usar el host virtual `api.localhost` (Traefik): añadir la línea al hosts:

```powershell
# Ejecutar PowerShell como Administrador y editar hosts
notepad $env:windir\System32\drivers\etc\hosts
# Añadir:
# 127.0.0.1    api.localhost
```

---

### 5) Ejecutar tests

Opción A — ejecutar localmente en un venv:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pytest -q
```

Opción B — ejecutar dentro del contenedor:

```powershell
docker compose -f .\servidor_docker\docker-compose.traefik.yml run --rm proyecto_api pytest -q
```

Notas:
- Algunas dependencias (weasyprint, lxml) requieren paquetes del sistema; si las pruebas fallan por dependencias nativas, usar la imagen Docker donde esos paquetes estén instalados.

---

### 6) Pasos siguientes recomendados (prioridad alta)

1. Añadir Flask‑Migrate e integrar en la app factory (`app/__init__.py`):
   - Agregar `Flask-Migrate` al `requirements.txt`.
   - Inicializar `Migrate` y generar la migración inicial (`flask db init`, `flask db migrate -m "initial"`, `flask db upgrade`).
   - Reemplazar `servidor_docker/init_db.py` por el flujo de migraciones.

2. Configurar CI (GitHub Actions):
   - Workflow que instale deps, corra `pytest`, y construya la imagen Docker en PRs.

3. Migrar a Postgres (dev/prod):
   - Añadir servicio `postgres` en `docker-compose` con volumen, cambiar `DATABASE_URL` en `.env` o en compose, y validar migraciones.

4. Revisión y limpieza del folder legacy `servidor-docker/`:
   - Si todo está correcto en `servidor_docker/`, archivar o eliminar la carpeta legacy con `scripts/cleanup-legacy.ps1`.

---

### 7) Checklist para la PR / revisión

- [ ] Confirmar que `docker compose up` levanta Traefik y `proyecto_api` correctamente.
- [ ] Ejecutar `init_db.py` (o aplicar migraciones) y confirmar que las tablas existen.
- [ ] Ejecutar `pytest` y corregir fallos. Documentar si hay tests débiles o dependientes de entorno.
- [ ] Añadir `Flask-Migrate` y generar la migración inicial (si se aprueba).
- [ ] Actualizar README con instrucciones simplificadas y badge de CI.
- [ ] Confirmar que no quedan imports rotos por nombres de archivos/carpetas (evitar guiones en nombres de paquetes).

---

### 8) Troubleshooting rápido

- ImportError por nombre de módulo: verificar que no exista carpeta con guion `servidor-docker` activa; usar `servidor_docker/` con `__init__.py`.
- RuntimeError SQLAlchemy app: usar la instancia `db` exportada por `app` y llamar `db.init_app(app)` (ya aplicado en `servidor_docker/app.py`).
- sqlite OperationalError (tabla ya existe): no ejecutar `create_all()` en import time; usar `init_db.py` o migraciones.
- Traefik en Windows no detecta provider.docker: la rama usa file-provider montado para dev (`traefik_dynamic.yml`).

---

### 9) Contacto / notas finales

Si querés, puedo:
- Implementar Flask‑Migrate y generar la migración inicial ahora.
- Crear un workflow de GitHub Actions para CI (tests + build).

Decime cuál de las dos tareas querés que haga antes de que subas la rama y que el compañero la tome.

---

Archivo creado por el equipo técnico — adaptad rutas/servicios si cambian los nombres de los contenedores.
