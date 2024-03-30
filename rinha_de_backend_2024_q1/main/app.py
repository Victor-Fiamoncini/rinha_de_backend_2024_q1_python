from config import config
from flask import Flask
from rinha_de_backend_2024_q1.main.blueprints import cli, router
from rinha_de_backend_2024_q1.main.extensions import database, migrate


def create_minimal_app(config_name: str) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    return app


def create_app(config_name: str) -> Flask:
    app = create_minimal_app(config_name)

    database.init_app(app)
    migrate.init_app(app)
    cli.init_app(app)
    router.init_app(app)

    return app
