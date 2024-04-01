from rinha_de_backend_2024_q1.app.repositories.create_transaction_repository import (
    CreateTransactionRepository,
)
from rinha_de_backend_2024_q1.app.repositories.get_client_by_id_repository import (
    GetClientByIdRepository,
)
from rinha_de_backend_2024_q1.app.repositories.update_client_repository import (
    UpdateClientRepository,
)
from rinha_de_backend_2024_q1.domain.entities.client_entity import (
    ClientEntity,
    MakeNewInput as MakeNewClientEntityInput,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    TransactionEntity,
)


class ClientRepositoryFake(GetClientByIdRepository, UpdateClientRepository):
    def get_client_by_id(self, client_id: int) -> ClientEntity:
        return ClientEntity.make_new(
            MakeNewClientEntityInput(id=1, limit=100_000, balance=0)
        )

    def update_client(self, client: ClientEntity):
        return


class TransactionRepositoryFake(CreateTransactionRepository):
    def create_transaction(self, transaction: TransactionEntity):
        return
