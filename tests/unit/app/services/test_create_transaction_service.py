from pytest import raises
from rinha_de_backend_2024_q1.app.exceptions import (
    InvalidInputException,
    RequiredInputException,
)
from rinha_de_backend_2024_q1.app.services.create_transaction_service import (
    CreateTransactionService,
)
from rinha_de_backend_2024_q1.domain.entities.client_entity import (
    ClientEntity,
    MakeNewInput as MakeNewClientEntityInput,
)
from rinha_de_backend_2024_q1.domain.exceptions import (
    ClientNotFoundException,
    InconsistentBalanceException,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import Input
from tests.unit.app.services.fakes import (
    ClientRepositoryFake,
    TransactionRepositoryFake,
)
from unittest.mock import Mock


def make_create_transaction_service():
    client_repository_mock = Mock(spec=ClientRepositoryFake)
    transaction_repository_mock = Mock(spec=TransactionRepositoryFake)

    sut = CreateTransactionService(
        get_client_by_id_repository=client_repository_mock,
        create_transaction_repository=transaction_repository_mock,
        update_client_repository=client_repository_mock,
    )

    return sut, client_repository_mock, transaction_repository_mock


def test_must_create_a_new_debit_transaction():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    client_repository_mock.get_client_by_id.return_value = ClientEntity.make_new(
        MakeNewClientEntityInput(id=1, limit=100_000, balance=0)
    )

    input = Input(client_id="1", value=1000, description="descricao", type_of="d")
    output = sut.create_transaction(input)

    assert output.limit == 100_000
    assert output.balance == -1000

    client_repository_mock.get_client_by_id.assert_called_once_with(1)
    transaction_repository_mock.create_transaction.assert_called_once()
    client_repository_mock.update_client.assert_called_once()


def test_must_create_a_new_credit_transaction():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    client_repository_mock.get_client_by_id.return_value = ClientEntity.make_new(
        MakeNewClientEntityInput(id=1, limit=100_000, balance=1000)
    )

    input = Input(client_id="1", value=2000, description="descricao", type_of="c")
    output = sut.create_transaction(input)

    assert output.limit == 100_000
    assert output.balance == 3000

    client_repository_mock.get_client_by_id.assert_called_once_with(1)
    transaction_repository_mock.create_transaction.assert_called_once()
    client_repository_mock.update_client.assert_called_once()


def test_must_raise_after_trying_to_create_a_debit_transaction_that_exceeds_the_client_limit():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    client_repository_mock.get_client_by_id.return_value = ClientEntity.make_new(
        MakeNewClientEntityInput(id=1, limit=50_000, balance=-40_000)
    )

    with raises(InconsistentBalanceException):
        input = Input(client_id="1", value=20_000, description="descricao", type_of="d")
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_called_once_with(1)
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_invalid_value():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    with raises(RequiredInputException):
        input = Input(client_id="1", value=None, description="descricao", type_of="d")  # type: ignore
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_not_called()
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()

    with raises(InvalidInputException):
        input = Input(client_id="1", value=-5000, description="descricao", type_of="c")
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_not_called()
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_invalid_description():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    with raises(RequiredInputException):
        input = Input(client_id="1", value=1000, description=None, type_of="d")  # type: ignore
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_not_called()
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()

    with raises(InvalidInputException):
        input = Input(
            client_id="1", value=5000, description="oooooooooooooo", type_of="c"
        )
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_not_called()
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_invalid_client_id_or_type():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    with raises(InvalidInputException):
        input = Input(client_id=None, value=1000, description="descricao", type_of="d")  # type: ignore
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_not_called()
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()

    with raises(InvalidInputException):
        input = Input(client_id="1", value=5000, description="descricao", type_of="A")
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_not_called()
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_a_non_existent_client():
    sut, client_repository_mock, transaction_repository_mock = (
        make_create_transaction_service()
    )

    client_repository_mock.get_client_by_id.return_value = None

    with raises(ClientNotFoundException):
        input = Input(
            client_id="9999", value=1000, description="descricao", type_of="d"
        )
        output = sut.create_transaction(input)

        assert output == None

    client_repository_mock.get_client_by_id.assert_called_once_with(9999)
    transaction_repository_mock.create_transaction.assert_not_called()
    client_repository_mock.update_client.assert_not_called()
