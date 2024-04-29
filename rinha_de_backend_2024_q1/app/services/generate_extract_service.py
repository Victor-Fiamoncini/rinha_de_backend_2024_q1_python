from datetime import datetime

from rinha_de_backend_2024_q1.app.exceptions import InvalidInputException
from rinha_de_backend_2024_q1.app.repositories.get_client_by_id_repository import (
    GetClientByIdRepository,
)
from rinha_de_backend_2024_q1.app.repositories.get_last_client_transactions_repository import (
    GetLastClientTransactionsRepository,
)
from rinha_de_backend_2024_q1.domain.exceptions import ClientNotFoundException
from rinha_de_backend_2024_q1.domain.usecases.generate_extract_usecase import (
    GenerateExtractUseCase,
    Output,
)


class GenerateExtractService(GenerateExtractUseCase):
    def __init__(
        self,
        get_client_by_id_repository: GetClientByIdRepository,
        get_last_client_transactions_repository: GetLastClientTransactionsRepository,
    ):
        super().__init__()

        self._get_client_by_id_repository = get_client_by_id_repository
        self._get_last_client_transactions_repository = (
            get_last_client_transactions_repository
        )

    def _validate_input(self, client_id: str):
        try:
            int(client_id)
        except:
            raise InvalidInputException("Client-id is invalid")

    def generate_extract(self, client_id: str) -> Output:
        self._validate_input(client_id)

        id = int(client_id)
        client = self._get_client_by_id_repository.get_client_by_id(id)

        if not client:
            raise ClientNotFoundException("Client not found")

        last_ten_transactions = (
            self._get_last_client_transactions_repository.get_last_ten_transactions(id)
        )

        return Output(
            balance=client.balance,
            created_at=datetime.now(),
            limit_of=client.limit,
            transactions=last_ten_transactions,
        )
