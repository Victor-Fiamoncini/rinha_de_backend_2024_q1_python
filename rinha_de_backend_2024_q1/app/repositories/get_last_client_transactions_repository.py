from abc import ABC, abstractmethod
from typing import List
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


class GetLastClientTransactionsRepository(ABC):
    @abstractmethod
    def get_last_ten_transactions(self, client_id: int) -> List[TransactionEntity]:
        pass
