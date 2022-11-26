import os

from quizlib.environment import ARTICLES_SITE, DATA_DIR

API_TOKEN = os.environ["API_TOKEN"]

__all__ = ["API_TOKEN", "ARTICLES_SITE", "DATA_DIR"]
