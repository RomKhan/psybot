#!/usr/bin/env -S PYTHONPATH=. python3

import json
from datetime import date
from glob import glob

from src.database import session
from src.environment import ARTICLES_SITE, DATA_DIR, WORDS_PER_MINUTE
from src.models import Article

session.query(Article).delete()

for file in glob(f"{DATA_DIR}/articles/*/*.json"):
    with open(file) as f:
        obj = json.load(f)

        del obj["docx_url"]
        obj["date"] = date.fromisoformat(obj["date"])
        obj["reading_time"] = round(len(obj["content"].split()) / WORDS_PER_MINUTE)
        obj["article_url"] = ARTICLES_SITE + obj.pop("url")

        if "featured_image" in obj:
            obj["image_url"] = ARTICLES_SITE + obj.pop("featured_image")

        session.add(Article(**obj))

session.commit()
