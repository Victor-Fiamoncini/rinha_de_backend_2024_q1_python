from flask.testing import FlaskClient


def test_must_get_a_successfull_response_from_health_check(client: FlaskClient):
    response = client.get("/health")
    response_text = response.data.decode("utf-8")

    assert response_text == "Server is alive!"
    assert response.status_code == 200
