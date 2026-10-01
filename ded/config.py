import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

BASE_DIR = Path(__file__).parent.parent


def _build_database_url():
    url = os.getenv('DATABASE_URL')
    if url:
        return url

    host = os.getenv('DATABASE_HOST', 'localhost')
    port = os.getenv('DATABASE_PORT', '5432')
    user = os.getenv('DATABASE_USER', 'postgres')
    password = os.getenv('DATABASE_PASSWORD', '')
    name = os.getenv('DATABASE_NAME', 'postgres')
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', "production-is-system-secret-key-change-me")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = 3600
    SQLALCHEMY_DATABASE_URI = _build_database_url()
    SQLALCHEMY_POOL_SIZE = int(os.getenv('SQLALCHEMY_POOL_SIZE', 10))
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', 20))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', 30))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', 3600))
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "TEST_DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/demo"
    )


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)