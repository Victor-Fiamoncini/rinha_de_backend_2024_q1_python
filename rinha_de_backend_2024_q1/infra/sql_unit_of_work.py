from types import TracebackType
from typing import Optional, Type

from rinha_de_backend_2024_q1.app.unit_of_work import UnitOfWork
from rinha_de_backend_2024_q1.main.extensions.database import db


class SqlUnitOfWork(UnitOfWork):
    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        if exc_type is None:
            db.session.commit()
        else:
            db.session.rollback()
