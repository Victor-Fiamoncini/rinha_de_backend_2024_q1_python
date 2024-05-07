from datetime import datetime

from rinha_de_backend_2024_q1.domain.entities.client_entity import ClientEntity
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


class TransactionEntityBuilder:
    def __init__(self):
        self.transaction_entity = TransactionEntity()

    def add_created_at(self, created_at: datetime) -> "TransactionEntityBuilder":
        self.transaction_entity.created_at = created_at
        return self

    def add_description(self, description: str) -> "TransactionEntityBuilder":
        self.transaction_entity.description = description
        return self

    def add_owner(self, owner: ClientEntity) -> "TransactionEntityBuilder":
        self.transaction_entity.owner = owner
        return self

    def add_type_of(self, type_of: str) -> "TransactionEntityBuilder":
        self.transaction_entity.type_of = type_of
        return self

    def add_value(self, value: int) -> "TransactionEntityBuilder":
        self.transaction_entity.value = value
        return self

    def build(self) -> TransactionEntity:
        return self.transaction_entity
