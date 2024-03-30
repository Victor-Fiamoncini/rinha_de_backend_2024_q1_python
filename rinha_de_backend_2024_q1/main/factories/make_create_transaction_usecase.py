from rinha_de_backend_2024_q1.app.services.create_transaction_service import (
    CreateTransactionService,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import (
    CreateTransactionUseCase,
)
from rinha_de_backend_2024_q1.infra.repositories.memory_client_repository import (
    MemoryClientRepository,
)
from rinha_de_backend_2024_q1.infra.repositories.memory_transaction_repository import (
    MemoryTransactionRepository,
)


def make_create_transaction_usecase() -> CreateTransactionUseCase:
    client_repository = MemoryClientRepository()
    transaction_repository = MemoryTransactionRepository()

    return CreateTransactionService(
        get_client_by_id_repository=client_repository,
        create_transaction_repository=transaction_repository,
        update_client_repository=client_repository,
    )
