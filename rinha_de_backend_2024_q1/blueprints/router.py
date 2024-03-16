from flask import Blueprint, Flask


bp = Blueprint("router", __name__)


@bp.route("/")
def hello_world():
    return "hello_world", 200


def init_app(app: Flask):
    app.register_blueprint(bp)
