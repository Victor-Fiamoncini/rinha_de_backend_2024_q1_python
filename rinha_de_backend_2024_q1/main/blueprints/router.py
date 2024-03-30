from flask import Blueprint, Flask, jsonify, request

bp = Blueprint("router", __name__)


@bp.get("/health")
def health_check():
    return "Server is alive!", 200


@bp.post("/clientes/<id>/transacoes")
def create_client_transaction(id: str):
    if not request.json:
        return jsonify({"message": "Invalid body type provided"}), 422

    client_id = None
    value = request.json.get("valor")
    description = request.json.get("descricao")
    type_of = request.json.get("tipo")

    return "", 200


def init_app(app: Flask):
    app.register_blueprint(bp)
