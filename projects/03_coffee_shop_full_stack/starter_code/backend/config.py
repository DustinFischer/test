import os

from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, os.getenv('DOT_ENV', '.env')))


def env(key, default=None):
    return os.getenv(key, default)


class Config(object):
    SECRET_KEY = env('SECRET_KEY', '30f18189f76b9ce6b2b3c85ced8d81989ff3af95fa1e7fd9')


class DevelopmentConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass
