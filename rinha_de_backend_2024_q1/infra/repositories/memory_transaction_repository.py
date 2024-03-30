from rinha_de_backend_2024_q1.app.repositories.create_transaction_repository import (
    CreateTransactionRepository,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


class MemoryTransactionRepository(CreateTransactionRepository):
    _transactions = []

    def create_transaction(self, transaction: TransactionEntity):
        self._transactions.append(
            {
                "value": transaction.value,
                "type_of": transaction.type_of,
                "description": transaction.description,
                "client_id": transaction.owner.id,
            }
        )
