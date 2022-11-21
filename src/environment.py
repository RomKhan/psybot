import os

API_TOKEN = os.environ["API_TOKEN"]
DATABASE_URI = os.environ["DATABASE_URI"]
ECHO_SQL = os.environ.get("ECHO_SQL", "False") == "True"
DATA_DIR = os.environ.get("DATA_DIR", "./data/")
ARTICLES_SITE = os.environ["ARTICLES_SITE"]
WORDS_PER_MINUTE = int(os.environ.get("WORDS_PER_MINUTE", "200"))
