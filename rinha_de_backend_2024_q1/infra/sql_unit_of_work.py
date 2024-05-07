from rinha_de_backend_2024_q1.app.unit_of_work import UnitOfWork
from rinha_de_backend_2024_q1.main.extensions.database import db


class SqlUnitOfWork(UnitOfWork):
    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
