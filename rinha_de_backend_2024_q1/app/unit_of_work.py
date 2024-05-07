from abc import ABC, abstractmethod
from types import TracebackType
from typing import Optional, Type


class UnitOfWork(ABC):
    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
