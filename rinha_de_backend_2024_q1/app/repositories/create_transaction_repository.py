from abc import ABC, abstractmethod
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


class CreateTransactionRepository(ABC):
    @abstractmethod
    def create_transaction(self, transaction: TransactionEntity):
        pass
