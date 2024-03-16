from flask import Flask

from rinha_de_backend_2024_q1.extensions import configuration


def minimal_app() -> Flask:
    app = Flask(__name__)
    configuration.init_app(app)

    return app


def create_app() -> Flask:
    app = minimal_app()
    configuration.load_extensions(app)

    return app
