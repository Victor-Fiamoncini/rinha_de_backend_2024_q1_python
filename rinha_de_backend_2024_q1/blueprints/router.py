from flask import Blueprint, Flask, jsonify


bp = Blueprint("router", __name__)


@bp.route("/health")
def health_check():
    return "Server is alive!", 200


def init_app(app: Flask):
    app.register_blueprint(bp)
