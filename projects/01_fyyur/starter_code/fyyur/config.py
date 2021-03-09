import os
from .utils import env

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.urandom(32)
    DEBUG = False
    TESTING = False

    # DB env variables
    DB_NAME = env('DB_NAME', default='fyyur')
    DB_USER = env('DB_USER', default='postgres')
    DB_PASSWORD = env('DB_PASSWORD', default='')
    DB_HOST = env('DB_HOST', default='127.0.0.1')
    DB_PORT = env('DB_PORT', default=5432)

    # SQLALchemy configs
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


class DevConfig(Config):
    DEBUG = True
    ENV = 'development'


class ProdConfig(Config):
    ENV = env('FLASK_ENV', default='production')
