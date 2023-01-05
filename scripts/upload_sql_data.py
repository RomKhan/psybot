#!/usr/bin/env python3

import json
from datetime import date
from glob import glob
from os.path import basename, splitext
from typing import Any
from urllib.parse import urljoin

from quizlib.database import engine, session
from quizlib.environment import ARTICLES_SITE, DATA_DIR, ECHO_SQL, QUIZ_DIR, WORDS_PER_MINUTE
from quizlib.models import Article, Fact, Quiz, Recommendation, Technique

engine.echo = ECHO_SQL


def object_assign(target: object, source: dict[str, Any]):
    for key in source:
        target.__setattr__(key, source[key])


def add_articles(Type: type[Article] | type[Technique], name: str):
    articles: list = session.query(Type).all()
    articles_dict = {(a.category, a.title): a for a in articles}
    for file in glob(f"{DATA_DIR}/{name}/*/*.json"):
        with open(file) as f:
            obj = json.load(f)

            del obj["docx_url"]
            obj["date"] = date.fromisoformat(obj["date"])
            obj["reading_time"] = round(len(obj["content"].split()) / WORDS_PER_MINUTE)
            obj["article_url"] = urljoin(ARTICLES_SITE, obj.pop("url"))

            if "featured_image" in obj:
                obj["image_url"] = urljoin(ARTICLES_SITE, obj.pop("featured_image"))

            key = (obj["category"], obj["title"])
            if key in articles_dict:
                object_assign(articles_dict[key], obj)
            else:
                session.add(Type(**obj))

    session.commit()


add_articles(Article, "articles")
add_articles(Technique, "techniques")

quizzes: list[Quiz] = session.query(Quiz).all()
quizzes_dict = {(a.category, a.filename): a for a in quizzes}
for file in glob(f"{QUIZ_DIR}/*/*.json"):
    with open(file) as f:
        obj = json.load(f)

        obj.pop("scales", None)
        obj["description"] = obj.pop("desc")

        for k in list(obj):
            if "_" in k:
                obj.pop(k)

        if "question" in obj:
            obj["questions"] = [obj.pop("question")]

        if "answers" in obj and isinstance(obj["answers"], dict):
            obj["answers"] = [list(obj["answers"].values())]

        key = (obj["category"], obj["filename"])
        if key in quizzes_dict:
            object_assign(quizzes_dict[key], obj)
        else:
            session.add(Quiz(**obj))

session.commit()

session.query(Fact).delete()  # todo
with open(f"{DATA_DIR}/facts.json") as f:
    facts = json.load(f)
    for author in facts:
        for fact in facts[author]:
            title = fact
            for sep in ["\n", ". ", " - ", " – ", " — "]:
                title = title.split(sep)[0]
            if len(title) > 100:
                title = None

            session.add(Fact(author=author, content=fact, title=title))

session.commit()

recommendations: list[Recommendation] = session.query(Recommendation).all()
recommendations_dict = {(a.category, a.title): a for a in recommendations}
for file in glob(f"{DATA_DIR}/recommendations/*.json"):
    with open(file) as f:
        arr = json.load(f)
        for item in arr:
            title = item["title"]
            category = splitext(basename(file))[0]
            item["category"] = category

            item["image_urls"] = [urljoin(ARTICLES_SITE, e) for e in item["image_urls"]]
            if not item["image_urls"]:
                del item["image_urls"]

            key = (category, title)
            key_json = (category + ".json", title)
            if key in recommendations_dict:
                object_assign(recommendations_dict[key], item)
            elif key_json in recommendations_dict:
                object_assign(recommendations_dict[key_json], item)
            else:
                session.add(Recommendation(**item))

session.commit()
