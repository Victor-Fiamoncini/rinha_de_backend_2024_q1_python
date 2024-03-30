from abc import ABC, abstractmethod

from rinha_de_backend_2024_q1.domain.entities.client_entity import ClientEntity


class UpdateClientRepository(ABC):
    @abstractmethod
    def update_client(self, client: ClientEntity):
        pass
