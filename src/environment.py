import os

from quizlib.environment import ARTICLES_SITE, DATA_DIR

API_TOKEN = os.environ["API_TOKEN"]
SERVER_URL = os.environ["SERVER_URL"]

__all__ = ["SERVER_URL", "API_TOKEN", "ARTICLES_SITE", "DATA_DIR"]
