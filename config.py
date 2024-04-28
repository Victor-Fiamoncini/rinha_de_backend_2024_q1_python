import os


class Config(object):
    DEBUG = False
    FLASK_RUN_PORT = 5000
    TESTING = False
    SQLALCHEMY_POOL_TIMEOUT = 30  # 30s


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://superuser:superpassword@postgres_dev/rinha_de_backend_dev"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://superuser:superpassword@postgres_test/rinha_de_backend_test"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
