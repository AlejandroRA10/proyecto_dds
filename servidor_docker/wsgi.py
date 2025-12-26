"""WSGI entrypoint para el contenedor de despliegue.

Se importa la factory/creador local `create_app` desde `servidor_docker.app`
y se expone la variable `app` para Gunicorn.
"""
from servidor_docker.app import create_app

app = create_app()
