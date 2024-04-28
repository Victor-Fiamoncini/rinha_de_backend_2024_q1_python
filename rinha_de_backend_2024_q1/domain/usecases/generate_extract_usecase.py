from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, TypedDict


class Transaction(TypedDict):
    description: str
    held_in: datetime
    type_of: Literal["c", "d"]
    value: int


@dataclass(frozen=True)
class Output:
    balance: int
    created_at: datetime
    limit_of: int
    transactions: List[Transaction]


class GenerateExtractUseCase(ABC):
    @abstractmethod
    def generate_extract(self, client_id: str) -> Output:
        pass
