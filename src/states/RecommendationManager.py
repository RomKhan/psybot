from dataclasses import dataclass
from ..database import Base
from functools import lru_cache
from ..database import session
import json
from quizlib.models import Course, Quiz, Technique, Fact, Article, ModelRecommendation
import urllib.request

URL_CONST = "https://psessence.ru/extapi/test/recommendations/"


@lru_cache
def get_article(id: int) -> Article:
    return session.query(Article).get(id)


@lru_cache
def get_course(id: int) -> Article:
    return session.query(Course).get(id)


@lru_cache
def get_quiz(id: int) -> Quiz:
    return session.query(Quiz).get(id)


@lru_cache
def get_technique(id: int) -> Quiz:
    return session.query(Technique).get(id)


@lru_cache
def get_fact(id: int) -> Quiz:
    return session.query(Fact).get(id)


@lru_cache
def get_recommendation_id(id: int, type: str) -> int:
    return session.query(ModelRecommendation.id) \
        .where(ModelRecommendation.internal_id == id, ModelRecommendation.type == type) \
        .one().id


class RecommendationManager:
    item_id: int
    type: str
    articles: list[Article]
    courses: list[Course]
    quizzes: list[Quiz]
    facts: list[Fact]
    techniques: list[Technique]
    url: str

    def __init__(self, item_id: int, type: str):
        self.item_id = item_id
        self.type = type
        self.articles = []
        self.courses = []
        self.quizzes = []
        self.facts = []
        self.techniques = []
        self.url = URL_CONST + str(get_recommendation_id(item_id, type))
        self.get_items()

    def get_articles_str(self) -> str:
        if len(self.articles) == 0:
            return ""
        res = []
        for article in self.articles:
            res.append(f'<a href="{article.article_url}">{article.title}</a>')
        return "\n".join(res)

    def get_techniques_str(self) -> str:
        if len(self.techniques) == 0:
            return ""
        res = []
        for t in self.techniques:
            res.append(f'<a href="{t.article_url}">{t.title}</a>')
        return "\n".join(res)


    def get_courses_str(self) -> str:
        if len(self.courses) == 0:
            return ""
        res = ["\n<b>Курсы:</b>\n"]
        for c in self.courses:
            res.append(f'Курс "{c.name}" (Доступен в разделе "Курсы"")')
        return "\n".join(res)

    def get_quizzes_str(self) -> str:
        if len(self.quizzes) == 0:
            return ""
        res = ["\n<b>Тесты</b>:\n"]
        for quiz in self.quizzes:
            res.append(f'Тест "{quiz.name}" (Доступен в категории {quiz.category}" раздела "Тесты")')
        return "\n".join(res)

    def get_facts_str(self) -> str:
        if len(self.facts) == 0:
            return ""
        res = ["\n<b>Интересные факты:</b>\n"]
        for fact in self.facts:
            res.append(f"— {fact.title}")
        return "\n".join(res)

    def get_message(self) -> str:
        res = ["Мы подобрали для вас интересные материалы, с которыми вы можете ознакомиться после {{STATE}}!\n\n"]
        res += ["<b>Дополнительные материалы для чтения:</b>\n",
                self.get_articles_str(),
                self.get_techniques_str(),
                self.get_courses_str(),
                self.get_quizzes_str(),
                self.get_facts_str()
                ]
        return "\n".join(res)

    def get_items(self):
        with urllib.request.urlopen(self.url) as response:
            body_json = response.read()
        body_dict = json.loads(body_json)
        for a in body_dict["articles"]:
            self.articles.append(get_article(a.get("id")))
        for c in body_dict["courses"]:
            self.courses.append(get_course(c.get("id")))
        for q in body_dict["quizzes"]:
            self.quizzes.append(get_quiz(q.get("id")))
        for f in body_dict["facts"]:
            self.facts.append(get_fact(f.get("id")))
        for t in body_dict["techniques"]:
            self.techniques.append(get_technique(t.get("id")))
