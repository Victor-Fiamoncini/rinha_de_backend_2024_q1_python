from typing import Union

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
from rinha_de_backend_2024_q1.infra.database.models import Client
from rinha_de_backend_2024_q1.main.extensions.database import db


class SqlClientRepository(GetClientByIdRepository, UpdateClientRepository):
    def get_client_by_id(self, client_id: int) -> Union[ClientEntity, None]:
        row = (
            db.session.query(Client.id, Client.limit_of, Client.balance)
            .filter_by(id=client_id)
            .first()
        )

        if not row:
            return None

        return ClientEntity.make_new(
            MakeNewInput(id=row.id, limit=row.limit_of, balance=row.balance)
        )

    def update_client(self, client: ClientEntity):
        row = db.session.query(Client).filter_by(id=client.id).first()

        if not row:
            raise Exception("Client not found")

        row.balance = client.balance
        row.limit_of = client.limit

        db.session.add(row)
        db.session.commit()
