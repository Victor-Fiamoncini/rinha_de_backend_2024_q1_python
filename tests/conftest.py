from flask import Flask
from pytest import fixture
from rinha_de_backend_2024_q1.infra.database.models import Client
from rinha_de_backend_2024_q1.main.app import create_app
from rinha_de_backend_2024_q1.main.extensions.database import db
from typing import Generator


def create_initial_clients():
    initial_limits = [100000, 80000, 1000000, 10000000, 500000]

    for limit in initial_limits:
        client = Client(limit_of=limit, balance=0)
        db.session.add(client)

    db.session.commit()


@fixture()
def app() -> Generator:
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        create_initial_clients()

        yield app

        db.session.close()
        db.drop_all()


@fixture()
def client(app: Flask) -> Generator:
    with app.test_client() as client:
        yield client
