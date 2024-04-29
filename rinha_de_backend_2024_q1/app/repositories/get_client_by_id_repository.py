from abc import ABC, abstractmethod
from typing import Union

from rinha_de_backend_2024_q1.domain.entities.client_entity import ClientEntity


class GetClientByIdRepository(ABC):
    @abstractmethod
    def get_client_by_id(self, client_id: int) -> Union[ClientEntity, None]:
        pass
