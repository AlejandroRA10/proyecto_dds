def init_db():
    """Inicializa la base de datos ejecutando create_all().

    Ejecutar dentro del contenedor:
    docker compose -f ./docker-compose.traefik.yml run --rm proyecto_api python -m servidor_docker.init_db
    """
    from servidor_docker.app import create_app
    from app import db

    app = create_app()
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    init_db()
