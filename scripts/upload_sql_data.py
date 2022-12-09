#!/usr/bin/env python3

import json
from datetime import date
from glob import glob
from os.path import basename
from urllib.parse import urljoin

from quizlib.database import engine, session
from quizlib.environment import ARTICLES_SITE, DATA_DIR, ECHO_SQL, QUIZ_DIR, WORDS_PER_MINUTE
from quizlib.models import Article, Fact, Quiz, Recommendation, Technique

engine.echo = ECHO_SQL


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
                for k in obj:
                    articles_dict[key].__setattr__(k, obj[k])
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
            for k in obj:
                quizzes_dict[key].__setattr__(k, obj[k])
        else:
            session.add(Quiz(**obj))

session.commit()

session.query(Fact).delete()  # todo
with open(f"{DATA_DIR}/facts.json") as f:
    facts = json.load(f)
    for author in facts:
        for fact in facts[author]:
            session.add(Fact(author=author, content=fact))

session.commit()

recommendations: list[Recommendation] = session.query(Recommendation).all()
recommendations_dict = {(a.category, a.title): a for a in recommendations}
for file in glob(f"{DATA_DIR}/recommendations/*.json"):
    with open(file) as f:
        obj = json.load(f)
        for title in obj:
            category = basename(file)

            key = (category, title)
            if key in recommendations_dict:
                recommendations_dict[key].content = obj[title]
            else:
                session.add(Recommendation(category=category, title=title, content=obj[title]))

session.commit()
