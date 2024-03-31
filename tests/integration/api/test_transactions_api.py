from flask.testing import FlaskClient


def test_must_create_a_debit_transaction_and_receive_client_balance_and_limit(
    client: FlaskClient,
):
    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 1000, "tipo": "d", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 200
    assert response.json["limite"] == 100000
    assert response.json["saldo"] == -1000


def test_must_fail_after_trying_to_create_a_debit_transaction_that_exceeds_the_client_limit(
    client: FlaskClient,
):
    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 200000, "tipo": "d", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 422
    assert (
        response.json["message"] == "The amount debited will exceed the client's limit"
    )


def test_must_create_a_credit_transaction_and_receive_client_balance_and_limit(
    client: FlaskClient,
):
    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 2000, "tipo": "c", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 200
    assert response.json["limite"] == 100000
    assert response.json["saldo"] == 2000


def test_must_receive_errors_after_send_invalid_fields(client: FlaskClient):
    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": "1000", "tipo": "d", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 400
    assert response.json["message"] == "Value is required"

    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": -1000, "tipo": "d", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 422
    assert response.json["message"] == "Value is invalid"

    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 1000, "tipo": "AAAAAAAA", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 422
    assert response.json["message"] == "Transaction type is invalid"

    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 1000, "tipo": "d", "descricao": None},
    )

    if not response.json:
        raise

    assert response.status_code == 400
    assert response.json["message"] == "Description is required"

    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 1000, "tipo": "d", "descricao": "descricaaAHAJSBDFIAUSFN"},
    )

    if not response.json:
        raise

    assert response.status_code == 422
    assert response.json["message"] == "Description is invalid"

    response = client.post(
        "/clientes/BSDIYABDF/transacoes",
        json={"valor": 1000, "tipo": "d", "descricao": "descricao"},
    )

    if not response.json:
        raise

    assert response.status_code == 422
    assert response.json["message"] == "Client-id is invalid"
