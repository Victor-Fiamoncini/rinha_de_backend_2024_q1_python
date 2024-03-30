from rinha_de_backend_2024_q1.app.repositories.get_client_by_id_repository import (
    GetClientByIdRepository,
)
from rinha_de_backend_2024_q1.app.repositories.update_client_repository import (
    UpdateClientRepository,
)
from rinha_de_backend_2024_q1.domain.entities.client_entity import (
    ClientEntity,
    MakeNewInput,
)


class MemoryClientRepository(GetClientByIdRepository, UpdateClientRepository):
    _clients = [
        {"id": 1, "limit_of": 100000, "balance": 0},
        {"id": 2, "limit_of": 80000, "balance": 0},
        {"id": 3, "limit_of": 1000000, "balance": 0},
        {"id": 4, "limit_of": 10000000, "balance": 0},
        {"id": 5, "limit_of": 500000, "balance": 0},
    ]

    def get_client_by_id(self, client_id: int) -> ClientEntity:
        client = next((c for c in self._clients if c["id"] == client_id), None)

        if not client:
            raise Exception("Client not found")

        return ClientEntity.make_new(
            MakeNewInput(
                id=client["id"], limit=client["limit_of"], balance=client["balance"]
            )
        )

    def update_client(self, client: ClientEntity):
        id_to_replace = client.id
        updated_client = {
            "id": client.id,
            "limit_of": client.limit,
            "balance": client.balance,
        }

        self._clients = [
            updated_client if c["id"] == id_to_replace else c for c in self._clients
        ]
