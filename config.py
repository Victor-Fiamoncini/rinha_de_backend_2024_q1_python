import os


class Config(object):
    DEBUG = False
    PORT = 5000
    TESTING = False


class ProductionConfig(Config):
    PORT = 8080
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
