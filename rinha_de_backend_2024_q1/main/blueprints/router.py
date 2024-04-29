from flask import Blueprint, Flask, jsonify, request

from rinha_de_backend_2024_q1.app.exceptions import (
    InvalidInputException,
    RequiredInputException,
)
from rinha_de_backend_2024_q1.domain.exceptions import (
    ClientNotFoundException,
    InconsistentBalanceException,
)
from rinha_de_backend_2024_q1.domain.usecases.create_transaction_usecase import (
    Input as CreateTransactionInput,
)
from rinha_de_backend_2024_q1.main.factories.make_create_transaction_usecase import (
    make_create_transaction_usecase,
)
from rinha_de_backend_2024_q1.main.factories.make_generate_extract_usecase import (
    make_generate_extract_usecase,
)

bp = Blueprint("router", __name__)


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

    create_transaction_usecase = make_create_transaction_usecase()

    try:
        output = create_transaction_usecase.create_transaction(
            CreateTransactionInput(
                client_id=id, value=value, description=description, type_of=type_of
            )
        )

        return jsonify({"limite": output.limit, "saldo": output.balance}), 200
    except ClientNotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except (InconsistentBalanceException, InvalidInputException) as e:
        return jsonify({"message": str(e)}), 422
    except RequiredInputException as e:
        return jsonify({"message": str(e)}), 400


@bp.get("/clientes/<id>/extrato")
def generate_client_extract(id: str):
    generate_extract_usecase = make_generate_extract_usecase()

    try:
        output = generate_extract_usecase.generate_extract(id)

        formatted_output = {
            "saldo": {
                "total": output.balance,
                "data_extrato": output.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                "limite": output.limit_of,
            },
            "ultimas_transacoes": [
                {
                    "valor": transaction.value,
                    "tipo": transaction.type_of,
                    "descricao": transaction.description,
                    "realizada_em": (
                        transaction.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                        if transaction.created_at
                        else None
                    ),
                }
                for transaction in output.transactions
            ],
        }

        return jsonify(formatted_output), 200
    except ClientNotFoundException as e:
        return jsonify({"message": str(e)}), 404
    except InvalidInputException as e:
        return jsonify({"message": str(e)}), 422


def init_app(app: Flask):
    app.register_blueprint(bp)
