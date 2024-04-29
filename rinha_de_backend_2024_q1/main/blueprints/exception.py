from logging import getLogger
from flask import Blueprint, Flask, jsonify


bp = Blueprint("exception", __name__)
logger = getLogger("exception_blueprint_logger")


@bp.errorhandler(Exception)
def handle_exception(e):
    logger.error(str(e))

    return jsonify({"message": "Internal error"}), 500


def init_app(app: Flask):
    app.register_blueprint(bp)
