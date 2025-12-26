"""Paquete de despliegue para la imagen Docker.

Este archivo hace que Python trate la carpeta `servidor_docker` como
un paquete; necesario para importar con `gunicorn servidor_docker.app:app`.
"""

__all__ = ["app"]
