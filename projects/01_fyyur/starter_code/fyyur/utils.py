import os


def env(key, default=None):
    return os.getenv(key, default)
