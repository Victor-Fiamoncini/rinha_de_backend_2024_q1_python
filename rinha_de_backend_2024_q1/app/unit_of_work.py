from abc import ABC
from types import TracebackType
from typing import Optional, Type


class UnitOfWork(ABC):
    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ):
        pass
