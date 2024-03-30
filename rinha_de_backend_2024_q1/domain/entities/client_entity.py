from dataclasses import dataclass

from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


@dataclass(frozen=True)
class MakeNewInput:
    id: int
    limit: int
    balance: int


class ClientEntity:
    def __init__(self, id: int, limit: int = 0, balance: int = 0):
        self.id = id
        self.limit = limit
        self.balance = balance

    @staticmethod
    def make_new(input: MakeNewInput) -> "ClientEntity":
        return ClientEntity(input.id, input.limit, input.balance)

    def update_balance_by_new_transaction(self, transaction: TransactionEntity):
        self.balance = self.balance - transaction.value
