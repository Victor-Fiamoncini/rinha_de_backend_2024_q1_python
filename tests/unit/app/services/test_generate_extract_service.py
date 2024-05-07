from datetime import datetime
from freezegun import freeze_time
from pytest import raises
from unittest.mock import Mock

from rinha_de_backend_2024_q1.app.exceptions import InvalidInputException
from rinha_de_backend_2024_q1.app.repositories.get_client_by_id_repository import (
    GetClientByIdRepository,
)
from rinha_de_backend_2024_q1.app.repositories.get_last_client_transactions_repository import (
    GetLastClientTransactionsRepository,
)
from rinha_de_backend_2024_q1.app.services.generate_extract_service import (
    GenerateExtractService,
)
from rinha_de_backend_2024_q1.domain.entities.client_entity import (
    ClientEntity,
    MakeNewInput,
)
from rinha_de_backend_2024_q1.domain.entities.transaction_entity import (
    GetWithoutOwnerInput,
    TransactionEntity,
)
from rinha_de_backend_2024_q1.domain.exceptions import ClientNotFoundException


def make_generate_extract_service():
    get_client_by_id_repository_mock = Mock(spec=GetClientByIdRepository)
    get_last_client_transactions_repository_mock = Mock(
        spec=GetLastClientTransactionsRepository
    )

    sut = GenerateExtractService(
        get_client_by_id_repository=get_client_by_id_repository_mock,
        get_last_client_transactions_repository=get_last_client_transactions_repository_mock,
    )

    return (
        sut,
        get_client_by_id_repository_mock,
        get_last_client_transactions_repository_mock,
    )


@freeze_time("2010-12-22")
def test_must_get_client_extract_successfully():
    (
        sut,
        get_client_by_id_repository_mock,
        get_last_client_transactions_repository_mock,
    ) = make_generate_extract_service()

    get_client_by_id_repository_mock.get_client_by_id.return_value = (
        ClientEntity.make_new(MakeNewInput(id=1, limit=100_000, balance=0))
    )

    last_ten_transactions = [
        TransactionEntity.get_without_owner(
            GetWithoutOwnerInput(
                created_at=datetime.now(),
                description="desc_01",
                type_of="c",
                value=100_000,
            )
        )
    ]
    get_last_client_transactions_repository_mock.get_last_ten_transactions.return_value = (
        last_ten_transactions
    )

    output = sut.generate_extract("1")

    assert output.balance == 0
    assert output.limit_of == 100_000
    assert output.transactions == last_ten_transactions
    assert output.created_at == datetime(2010, 12, 22)

    get_client_by_id_repository_mock.get_client_by_id.assert_called_once_with(1)
    get_last_client_transactions_repository_mock.get_last_ten_transactions(1)


def test_must_raise_after_trying_to_generate_extract_with_invalid_client_id():
    (
        sut,
        get_client_by_id_repository_mock,
        get_last_client_transactions_repository_mock,
    ) = make_generate_extract_service()

    with raises(InvalidInputException):
        output = sut.generate_extract(None)  # type: ignore

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    get_last_client_transactions_repository_mock.get_last_ten_transactions.assert_not_called()


def test_must_raise_after_trying_to_generate_extract_with_a_non_existent_client():
    (
        sut,
        get_client_by_id_repository_mock,
        get_last_client_transactions_repository_mock,
    ) = make_generate_extract_service()

    get_client_by_id_repository_mock.get_client_by_id.return_value = None

    with raises(ClientNotFoundException):
        output = sut.generate_extract("9999")

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_called_once_with(9999)
    get_last_client_transactions_repository_mock.get_last_ten_transactions.assert_not_called()
