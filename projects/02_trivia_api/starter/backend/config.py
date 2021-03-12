import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, os.getenv('DOT_ENV', '.env')))


def env(key, default=None):
    return os.getenv(key, default)


class Config(object):
    SECRET_KEY = env('SECRET_KEY', '30f18189f76b9ce6b2b3c85ced8d81989ff3af95fa1e7fd9')

    # SQLAlchemy

    # DB env variables
    DB_NAME = env('DB_NAME', default='trivia')
    DB_USER = env('DB_USER', default='postgres')
    DB_PASSWORD = env('DB_PASSWORD', default='')
    DB_HOST = env('DB_HOST', default='127.0.0.1')
    DB_PORT = env('DB_PORT', default=5432)

    # SQLAlchemy configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    # Silence the deprecation warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass
