from rinha_de_backend_2024_q1.app.exceptions.invalid_input_exception import (
    InvalidInputException,
)
from rinha_de_backend_2024_q1.app.repositories.create_transaction_repository import (
    CreateTransactionRepository,
)
from rinha_de_backend_2024_q1.app.repositories.get_client_by_id_repository import (
    GetClientByIdRepository,
)
from rinha_de_backend_2024_q1.app.repositories.update_client_repository import (
    UpdateClientRepository,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    MakeNewInput,
    TransactionEntity,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import (
    CreateTransactionUseCase,
    Input,
    Output,
)


class CreateTransactionService(CreateTransactionUseCase):
    def __init__(
        self,
        get_client_by_id_repository: GetClientByIdRepository,
        create_transaction_repository: CreateTransactionRepository,
        update_client_repository: UpdateClientRepository,
    ):
        super().__init__()

        self._get_client_by_id_repository = get_client_by_id_repository
        self._create_transaction_repository = create_transaction_repository
        self._update_client_repository = update_client_repository

    def _validate_input(self, input: Input):
        if not isinstance(input.value, int):
            raise InvalidInputException("Invalid value")

        if input.value <= 0:
            raise InvalidInputException("Invalid value")

        if input.type_of not in ["c", "d"]:
            raise InvalidInputException("Invalid transaction type")

        if not isinstance(input.description, str):
            raise InvalidInputException("Invalid description")

        if len(input.description) < 1 or len(input.description) > 10:
            raise InvalidInputException("Invalid description")

        try:
            int(input.client_id)
        except:
            raise InvalidInputException("Invalid client id provided")

    def create_transaction(self, input: Input) -> Output:
        self._validate_input(input)

        client = self._get_client_by_id_repository.get_client_by_id(
            int(input.client_id)
        )

        transaction = TransactionEntity.make_new(
            MakeNewInput(
                value=input.value,
                type_of=input.type_of,
                description=input.description,
                owner=client,
            )
        )

        client.update_balance_by_new_transaction(transaction)

        self._create_transaction_repository.create_transaction(transaction)
        self._update_client_repository.update_client(client)

        return Output(limit=client.limit, balance=client.balance)
