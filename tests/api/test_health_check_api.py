from rinha_de_backend_2024_q1.app import create_app


def test_must_get_a_successfull_response_from_health_check():
    app = create_app()

    response = app.test_client().get("/health")
    response_text = response.data.decode("utf-8")

    assert response_text == "Server is alive!"
    assert response.status_code == 200
