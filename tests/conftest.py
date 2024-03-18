import pytest
from flask.testing import FlaskClient
from flask import Flask
from rinha_de_backend_2024_q1.app import create_app
from typing import Generator


@pytest.fixture()
def app() -> Generator:
    app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
