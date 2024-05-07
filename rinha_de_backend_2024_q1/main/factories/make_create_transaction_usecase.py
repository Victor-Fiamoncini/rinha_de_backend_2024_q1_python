from rinha_de_backend_2024_q1.app.services.create_transaction_service import (
    CreateTransactionService,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import (
    CreateTransactionUseCase,
)
from rinha_de_backend_2024_q1.infra.repositories.sql_client_repository import (
    SqlClientRepository,
)
from rinha_de_backend_2024_q1.infra.repositories.sql_transaction_respository import (
    SqlTransactionRepository,
)
from rinha_de_backend_2024_q1.infra.sql_unit_of_work import SqlUnitOfWork


def make_create_transaction_usecase() -> CreateTransactionUseCase:
    client_repository = SqlClientRepository()
    transaction_repository = SqlTransactionRepository()

    return CreateTransactionService(
        unit_of_work=SqlUnitOfWork(),
        get_client_by_id_repository=client_repository,
        create_transaction_repository=transaction_repository,
        update_client_repository=client_repository,
    )
