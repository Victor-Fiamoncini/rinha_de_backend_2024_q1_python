from flask import Blueprint, Flask
from rinha_de_backend_2024_q1.infra.database.models import Client
from rinha_de_backend_2024_q1.main.extensions.database import db


bp = Blueprint("cli", __name__)


@bp.cli.command("create-database")
def create_database():
    db.create_all()


@bp.cli.command("create-clients")
def create_initial_clients():
    initial_limits = [100000, 80000, 1000000, 10000000, 500000]

    for limit in initial_limits:
        client = Client(limit_of=limit, balance=0)
        db.session.add(client)

    db.session.commit()


def init_app(app: Flask):
    app.register_blueprint(bp)
