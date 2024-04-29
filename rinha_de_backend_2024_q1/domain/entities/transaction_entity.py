from dataclasses import dataclass
from datetime import datetime
from rinha_de_backend_2024_q1.domain.exceptions import InconsistentBalanceException


@dataclass(frozen=True)
class MakeNewInput:
    description: str
    owner: "ClientEntity"
    type_of: str
    value: int


@dataclass(frozen=True)
class GetWithoutOwnerInput:
    created_at: datetime
    description: str
    type_of: str
    value: int


class TransactionEntity:
    def __init__(self):
        self.created_at = None
        self.description = None
        self.owner = None
        self.type_of = None
        self.value = None

    @staticmethod
    def make_new(input: MakeNewInput) -> "TransactionEntity":
        if input.type_of == "d":
            new_balance = input.owner.balance - input.value

            if new_balance < (input.owner.limit * -1):
                raise InconsistentBalanceException(
                    "The amount debited will exceed the client's limit"
                )

        return (
            TransactionEntityBuilder()
            .add_description(input.description)
            .add_owner(input.owner)
            .add_type_of(input.type_of)
            .add_value(input.value)
            .build()
        )

    @staticmethod
    def get_without_owner(input: GetWithoutOwnerInput) -> "TransactionEntity":
        return (
            TransactionEntityBuilder()
            .add_created_at(input.created_at)
            .add_description(input.description)
            .add_type_of(input.type_of)
            .add_value(input.value)
            .build()
        )


from rinha_de_backend_2024_q1.domain.entities.client_entity import ClientEntity
from rinha_de_backend_2024_q1.domain.builders.transaction_entity_builder import (
    TransactionEntityBuilder,
)
