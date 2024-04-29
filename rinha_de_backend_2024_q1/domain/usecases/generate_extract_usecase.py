from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


@dataclass(frozen=True)
class Output:
    balance: int
    created_at: datetime
    limit_of: int
    transactions: List[TransactionEntity]


class GenerateExtractUseCase(ABC):
    @abstractmethod
    def generate_extract(self, client_id: str) -> Output:
        pass
