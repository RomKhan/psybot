import time
from functools import lru_cache
from typing import Collection
from urllib.parse import urlencode

from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

# from main import dp
from .RecommendationManager import RecommendationManager
import markdown
from quizlib.util import hmac_sign
from ..database import session
from ..environment import SERVER_URL
from ..models import Article, Technique
from ..util import ReplyMarkupType
from .CategoryState import Categorizable, CategoryState
from .LikeableState import LikeableState


@lru_cache
def list_articles() -> list[tuple[int, str, str, bool]]:
    columns = [Article.id, Article.category, Article.title, Article.needs_subscription]
    return session.query(*columns).distinct().all()


@lru_cache
def list_categories() -> Collection[str]:
    return set(e[1] for e in list_articles())


@lru_cache
def articles_by_cat(category: str) -> list[Categorizable]:
    return [
        Categorizable(id, cat, title, sub)
        for id, cat, title, sub in list_articles()
        if cat == category
    ]


@lru_cache
def get_article(id: int) -> Article:
    return session.query(Article).get(id)


def get_article_url(article: Article | Technique) -> str:
    if not article.needs_subscription:
        return article.article_url

    data: dict[str, str] = {}
    data["id"] = str(article.id)
    data["date"] = str(int(time.time()))
    data["signature"] = hmac_sign(data)
    return f"{SERVER_URL}exclusive/article?{urlencode(data)}"


class ArticleCategoryState(CategoryState):
    name = "ArticleCategory"
    random_button = "Случайная статья"
    item_name = "Статья"
    recommendation_message = ""

    selected_article: Article | Technique | None = None

    def get_items(self) -> list[Categorizable]:
        return articles_by_cat(self.category)

    def get_article(self) -> Article | Technique:
        return get_article(self.items[self.item_number].id)

    def print_recommendation(self) -> str:
        try:
            manager = RecommendationManager(self.selected_article.id, "Article")
            return manager.get_message().replace("{{STATE}}", "прочтения статьи")
        except (Exception,):
            return ""

    def print_item(self) -> str:
        article = self.get_article()
        if article.needs_subscription and not self.is_subscribed:
            return self.data["message403"]
        self.need_recommendation = True
        self.mark_as_read(article)
        self.recommendation_message = self.print_recommendation()
        text = " ".join(article.content.split()[:50])
        res = [
            f'<a href="{article.image_url}">  </a>',
            f"{self.item_name} №{self.item_number + 1} в категории «{self.category}»",
            markdown.markdown(article.title)[3:][:-4],
            markdown.markdown(text)[3:][:-4],
            f"Читать полную весрию: {get_article_url(article)}",

        ]
        return "\n\n".join(res)

    def get_buttons(self) -> ReplyMarkupType:
        # todo: use both keyboards
        if self.selected_article:
            res = ArticleState.likes_keyboard(self.selected_article)
            return res
        return super().get_buttons()

    def mark_as_read(self, article: Article | Technique) -> None:
        article.view(self.user.id)
        self.selected_article = article


class ArticleState(LikeableState):
    name = "Articles"
    substate = ArticleCategoryState

    def list_categories(self) -> Collection[str]:
        return list_categories()

    def get_item(self, id: int) -> Article:
        return get_article(id)
