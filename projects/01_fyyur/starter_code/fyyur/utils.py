import os

from flask import flash


def env(key, default=None):
    return os.getenv(key, default)
