from flask import Flask
from pytest import fixture
from rinha_de_backend_2024_q1.app import create_app
from rinha_de_backend_2024_q1.extensions.database import db
from rinha_de_backend_2024_q1.models import Client
from typing import Generator


def create_initial_clients():
    initial_limits = [100000, 80000, 1000000, 10000000, 500000]

    for limit in initial_limits:
        client = Client(limit=limit, balance=0)
        db.session.add(client)

    db.session.commit()


@fixture(scope="session")
def app() -> Generator:
    app = create_app(FORCE_ENV_FOR_DYNACONF="testing")

    with app.app_context():
        db.create_all()
        create_initial_clients()

        yield app

        db.drop_all()


@fixture(scope="session")
def client(app: Flask) -> Generator:
    with app.test_client() as client:
        yield client
