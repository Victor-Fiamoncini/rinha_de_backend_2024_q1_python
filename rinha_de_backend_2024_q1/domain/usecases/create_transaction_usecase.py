from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Input:
    client_id: int
    value: int
    description: str
    type_of: str


@dataclass(frozen=True)
class Output:
    limit: int
    balance: int


class CreateTransactionUseCase(ABC):
    @abstractmethod
    def create_transaction(self, input: Input) -> Output:
        pass
