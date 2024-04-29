from typing import List
from rinha_de_backend_2024_q1.app.repositories.create_transaction_repository import (
    CreateTransactionRepository,
)
from rinha_de_backend_2024_q1.app.repositories.get_last_client_transactions_repository import (
    GetLastClientTransactionsRepository,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    GetWithoutOwnerInput,
    TransactionEntity,
)
from rinha_de_backend_2024_q1.infra.database.models import Transaction
from rinha_de_backend_2024_q1.main.extensions.database import db


class SqlTransactionRepository(
    CreateTransactionRepository, GetLastClientTransactionsRepository
):
    def create_transaction(self, transaction: TransactionEntity):
        if not transaction.owner:
            raise Exception("Transaction owner not provided")

        new_row = Transaction(
            value=transaction.value,
            type_of=transaction.type_of,
            description=transaction.description,
            client_id=transaction.owner.id,
        )

        db.session.add(new_row)
        db.session.commit()

    def get_last_ten_transactions(self, client_id: int) -> List[TransactionEntity]:
        rows = (
            db.session.query(
                Transaction.created_at,
                Transaction.description,
                Transaction.type_of,
                Transaction.value,
            )
            .filter_by(client_id=client_id)
            .order_by(Transaction.created_at.desc())
            .limit(10)
        )

        return [
            TransactionEntity.get_without_owner(
                GetWithoutOwnerInput(
                    created_at=row.created_at,
                    description=row.description,
                    type_of=row.type_of,
                    value=row.value,
                )
            )
            for row in rows
        ]
