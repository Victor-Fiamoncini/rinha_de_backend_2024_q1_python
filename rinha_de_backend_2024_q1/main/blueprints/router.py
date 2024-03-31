from flask import Blueprint, Flask, jsonify, request
from logging import getLogger
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

bp = Blueprint("router", __name__)
logger = getLogger("router_blueprint_logger")


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
        create_transaction_usecase = make_create_transaction_usecase()
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
    except Exception as e:
        logger.error(str(e))

        return jsonify({"message": "Internal error"}), 500


def init_app(app: Flask):
    app.register_blueprint(bp)
