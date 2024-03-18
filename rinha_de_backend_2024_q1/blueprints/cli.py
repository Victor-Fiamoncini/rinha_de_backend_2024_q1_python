from flask import Blueprint, Flask
from rinha_de_backend_2024_q1.extensions.database import db
from rinha_de_backend_2024_q1.models import Client


bp = Blueprint("cli", __name__)


@bp.cli.command("create-database")
def create_database():
    db.create_all()


@bp.cli.command("create-clients")
def create_clients():
    for limit, initial_balance in [
        (100000, 0),
        (80000, 0),
        (1000000, 0),
        (10000000, 0),
        (500000, 0),
    ]:
        client = Client(limit=limit, balance=initial_balance)
        db.session.add(client)

    db.session.commit()


def init_app(app: Flask):
    app.register_blueprint(bp)
