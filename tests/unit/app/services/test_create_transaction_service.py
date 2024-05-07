from pytest import raises
from unittest.mock import MagicMock, Mock

from rinha_de_backend_2024_q1.app.exceptions import (
    InvalidInputException,
    RequiredInputException,
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
from rinha_de_backend_2024_q1.app.services.create_transaction_service import (
    CreateTransactionService,
)
from rinha_de_backend_2024_q1.app.unit_of_work import UnitOfWork
from rinha_de_backend_2024_q1.domain.entities.client_entity import (
    ClientEntity,
    MakeNewInput as MakeNewClientEntityInput,
)
from rinha_de_backend_2024_q1.domain.exceptions import (
    ClientNotFoundException,
    InconsistentBalanceException,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import Input


def make_create_transaction_service():
    unit_of_work_mock = MagicMock(spec=UnitOfWork)
    get_client_by_id_repository_mock = Mock(spec=GetClientByIdRepository)
    create_transaction_repository_mock = Mock(spec=CreateTransactionRepository)
    update_client_repository_mock = Mock(spec=UpdateClientRepository)

    sut = CreateTransactionService(
        unit_of_work=unit_of_work_mock,
        get_client_by_id_repository=get_client_by_id_repository_mock,
        create_transaction_repository=create_transaction_repository_mock,
        update_client_repository=update_client_repository_mock,
    )

    return (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    )


def test_must_create_a_new_debit_transaction():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    get_client_by_id_repository_mock.get_client_by_id.return_value = (
        ClientEntity.make_new(MakeNewClientEntityInput(id=1, limit=100_000, balance=0))
    )

    input = Input(client_id="1", value=1000, description="descricao", type_of="d")
    output = sut.create_transaction(input)

    assert output.limit == 100_000
    assert output.balance == -1000

    get_client_by_id_repository_mock.get_client_by_id.assert_called_once_with(1)
    create_transaction_repository_mock.create_transaction.assert_called_once()
    update_client_repository_mock.update_client.assert_called_once()


def test_must_create_a_new_credit_transaction():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    get_client_by_id_repository_mock.get_client_by_id.return_value = (
        ClientEntity.make_new(
            MakeNewClientEntityInput(id=1, limit=100_000, balance=1000)
        )
    )

    input = Input(client_id="1", value=2000, description="descricao", type_of="c")
    output = sut.create_transaction(input)

    assert output.limit == 100_000
    assert output.balance == 3000

    get_client_by_id_repository_mock.get_client_by_id.assert_called_once_with(1)
    create_transaction_repository_mock.create_transaction.assert_called_once()
    update_client_repository_mock.update_client.assert_called_once()


def test_must_raise_after_trying_to_create_a_debit_transaction_that_exceeds_the_client_limit():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    get_client_by_id_repository_mock.get_client_by_id.return_value = (
        ClientEntity.make_new(
            MakeNewClientEntityInput(id=1, limit=50_000, balance=-40_000)
        )
    )

    with raises(InconsistentBalanceException):
        input = Input(client_id="1", value=20_000, description="descricao", type_of="d")
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_called_once_with(1)
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_invalid_value():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    with raises(RequiredInputException):
        input = Input(client_id="1", value=None, description="descricao", type_of="d")  # type: ignore
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()

    with raises(InvalidInputException):
        input = Input(client_id="1", value=-5000, description="descricao", type_of="c")
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_invalid_description():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    with raises(RequiredInputException):
        input = Input(client_id="1", value=1000, description=None, type_of="d")  # type: ignore
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()

    with raises(InvalidInputException):
        input = Input(
            client_id="1", value=5000, description="oooooooooooooo", type_of="c"
        )
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_invalid_client_id_or_type():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    with raises(InvalidInputException):
        input = Input(client_id=None, value=1000, description="descricao", type_of="d")  # type: ignore
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()

    with raises(InvalidInputException):
        input = Input(client_id="1", value=5000, description="descricao", type_of="A")
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_not_called()
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()


def test_must_raise_after_trying_to_create_a_transaction_with_a_non_existent_client():
    (
        sut,
        get_client_by_id_repository_mock,
        create_transaction_repository_mock,
        update_client_repository_mock,
    ) = make_create_transaction_service()

    get_client_by_id_repository_mock.get_client_by_id.return_value = None

    with raises(ClientNotFoundException):
        input = Input(
            client_id="9999", value=1000, description="descricao", type_of="d"
        )
        output = sut.create_transaction(input)

        assert output == None

    get_client_by_id_repository_mock.get_client_by_id.assert_called_once_with(9999)
    create_transaction_repository_mock.create_transaction.assert_not_called()
    update_client_repository_mock.update_client.assert_not_called()
