import os


class Config():
    DEBUG = False
    TESTING = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = [
        "access",
        "refresh",
    ]


class ProductionConfig(Config):
    MONGODB_SETTINGS = {
        'host': os.environ.get("DATABASE_URL")
    }


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'payment-db',
        'host': os.environ.get("DATABASE_URL"),
        'connect': False
    }


class TestingConfig(Config):
    TESTING = True
