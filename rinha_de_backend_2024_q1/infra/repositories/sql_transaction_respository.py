from rinha_de_backend_2024_q1.app.repositories.create_transaction_repository import (
    CreateTransactionRepository,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)
from rinha_de_backend_2024_q1.infra.database.models import Transaction
from rinha_de_backend_2024_q1.main.extensions.database import db


class SqlTransactionRepository(CreateTransactionRepository):
    def create_transaction(self, transaction: TransactionEntity):
        new_row = Transaction(
            value=transaction.value,
            type_of=transaction.type_of,
            description=transaction.description,
            client_id=transaction.owner.id,
        )

        db.session.add(new_row)
        db.session.commit()
