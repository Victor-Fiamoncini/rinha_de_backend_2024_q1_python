from flask import Flask

from rinha_de_backend_2024_q1.extensions import configuration


def create_minimal_app(**config) -> Flask:
    app = Flask(__name__)
    configuration.init_app(app, **config)

    return app


def create_app(**config) -> Flask:
    app = create_minimal_app(**config)
    configuration.load_extensions(app)

    return app
