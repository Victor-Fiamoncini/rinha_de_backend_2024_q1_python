from abc import ABC, abstractmethod

from rinha_de_backend_2024_q1.domain.entities.client_entity import ClientEntity


class GetClientByIdRepository(ABC):
    @abstractmethod
    def get_client_by_id(self, client_id: int) -> ClientEntity:
        pass
