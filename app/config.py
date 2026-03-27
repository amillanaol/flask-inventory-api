import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres:postgres@localhost:5432/inventory_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None

    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    ITEMS_PER_PAGE = 10


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
