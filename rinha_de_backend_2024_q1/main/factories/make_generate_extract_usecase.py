from rinha_de_backend_2024_q1.app.services.generate_extract_service import (
    GenerateExtractService,
)
from rinha_de_backend_2024_q1.domain.usecases.generate_extract_usecase import (
    GenerateExtractUseCase,
)
from rinha_de_backend_2024_q1.infra.repositories.sql_client_repository import (
    SqlClientRepository,
)
from rinha_de_backend_2024_q1.infra.repositories.sql_transaction_respository import (
    SqlTransactionRepository,
)


def make_generate_extract_usecase() -> GenerateExtractUseCase:
    client_repository = SqlClientRepository()
    transaction_repository = SqlTransactionRepository()

    return GenerateExtractService(
        get_client_by_id_repository=client_repository,
        get_last_client_transactions_repository=transaction_repository,
    )
