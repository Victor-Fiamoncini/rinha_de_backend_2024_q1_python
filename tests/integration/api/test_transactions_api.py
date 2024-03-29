from flask.testing import FlaskClient


def test_must_create_a_transaction_and_update_the_client_balance(client: FlaskClient):
    response = client.post(
        "/clientes/1/transacoes",
        json={"valor": 1000, "tipo": "c", "descricao": "descricao"},
    )

    assert response.status_code == 200
