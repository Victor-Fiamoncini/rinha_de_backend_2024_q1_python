from typing import List

from rinha_de_backend_2024_q1.app.repositories.create_transaction_repository import (
    CreateTransactionRepository,
)
from rinha_de_backend_2024_q1.app.repositories.get_last_client_transactions_repository import (
    GetLastClientTransactionsRepository,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


class MemoryTransactionRepository(
    CreateTransactionRepository, GetLastClientTransactionsRepository
):
    _transactions = []

    def create_transaction(self, transaction: TransactionEntity):
        if not transaction.owner:
            raise Exception("Transaction owner not provided")

        self._transactions.append(
            {
                "value": transaction.value,
                "type_of": transaction.type_of,
                "description": transaction.description,
                "client_id": transaction.owner.id,
            }
        )

    def get_last_ten_transactions(self, client_id: int) -> List[TransactionEntity]:
        return []
