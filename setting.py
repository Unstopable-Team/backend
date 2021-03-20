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
    WATTSIGHT_CLIENT_ID = os.environ.get("WATTSIGHT_CLIENT_ID")
    WATTSIGHT_CLIENT_SECRET = os.environ.get("WATTSIGHT_CLIENT_SECRET")
    ENTSOE_API_TOKEN = os.environ.get("ENTSOE_API_TOKEN")


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {
        'db': 'payment-db',
        'host': os.environ.get("DATABASE_URL"),
        'connect': False
    }
    WATTSIGHT_CLIENT_ID = os.environ.get("WATTSIGHT_CLIENT_ID")
    WATTSIGHT_CLIENT_SECRET = os.environ.get("WATTSIGHT_CLIENT_SECRET")
    ENTSOE_API_TOKEN = os.environ.get("ENTSOE_API_TOKEN")


class TestingConfig(Config):
    TESTING = True
