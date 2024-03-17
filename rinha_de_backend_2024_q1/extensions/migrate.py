from flask import Flask
from flask_migrate import Migrate
from rinha_de_backend_2024_q1.extensions.database import db


def init_app(app: Flask):
    Migrate(app, db)
