from flask import Blueprint, Flask, jsonify, request
from rinha_de_backend_2024_q1.app.exceptions.invalid_input_exception import (
    InvalidInputException,
)
from rinha_de_backend_2024_q1.domain.exceptions.inconsistent_balance_exception import (
    InconsistentBalanceException,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import Input
from rinha_de_backend_2024_q1.main.factories.make_create_transaction_usecase import (
    make_create_transaction_usecase,
)

bp = Blueprint("router", __name__)

create_transaction_usecase = make_create_transaction_usecase()


@bp.get("/health")
def health_check():
    return "Server is alive!", 200


@bp.post("/clientes/<id>/transacoes")
def create_client_transaction(id: str):
    if not request.json:
        return jsonify({"message": "Invalid body type provided"}), 422

    value = request.json.get("valor")
    description = request.json.get("descricao")
    type_of = request.json.get("tipo")

    try:
        input = Input(
            client_id=id, value=value, description=description, type_of=type_of
        )
        output = create_transaction_usecase.create_transaction(input)

        return jsonify({"limite": output.limit, "saldo": output.balance}), 200
    except InconsistentBalanceException as e:
        return jsonify({"message": str(e)}), 422
    except InvalidInputException as e:
        return jsonify({"message": str(e)}), 400


def init_app(app: Flask):
    app.register_blueprint(bp)
