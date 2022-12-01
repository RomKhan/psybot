from functools import lru_cache
from typing import Collection

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..database import session
from ..models import Article, User
from ..util import ReplyMarkupType, flatten
from .BaseState import BaseState
from .PageableState import PageableState


@lru_cache
def list_articles() -> list[tuple[int, str, str, bool]]:
    columns = [Article.id, Article.category, Article.title, Article.needs_subscription]
    return session.query(*columns).distinct().all()


@lru_cache
def list_categories() -> Collection[str]:
    return set(e[1] for e in list_articles())


@lru_cache
def articles_by_cat(category: str, subscription: bool = False) -> list[tuple[int, str]]:
    return [
        (id, title)
        for id, cat, title, sub in list_articles()
        if cat == category and (subscription or not sub)
    ]


@lru_cache
def get_article(id: int) -> Article:
    return session.query(Article).get(id)


def get_keyboard_for_article(article: Article) -> InlineKeyboardMarkup:
    id = article.id
    likes = article.likes
    dislikes = -likes if likes < 0 else ""
    likes = likes if likes > 0 else ""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"👍 {likes}", callback_data=f"Articles/like:{id}"),
                InlineKeyboardButton(text=f"👎 {dislikes}", callback_data=f"Articles/dislike:{id}"),
            ]
        ],
    )


class ArticleCategoryState(PageableState):
    category: str
    name = "ArticleCategory"
    random_button = "Случайная статья"
    start_button = ""
    is_random = False

    items: list[tuple[int, str]]
    selected_article: Article | None

    def get_items(self) -> list[tuple[int, str]]:
        return articles_by_cat(self.category, self.user.is_subscribed())

    def get_headline(self, article: tuple[int, str]) -> str:
        return article[1]

    def print_item(self) -> str:
        article = get_article(self.items[self.item_number][0])
        self.mark_as_read(article)
        text = " ".join(article.content.split()[:50])
        res = [
            f"Статья №{self.item_number+1} в категории «{self.category}»",
            article.title,
            text,
            f"Чиатать полную весрию: {article.article_url}",
        ]
        return "\n\n".join(res)

    def __init__(self, user: User, text: str) -> None:
        self.category = ""
        self.selected_article = None
        super().__init__(user, text)

    def set_substate(self, *args: str) -> None:
        assert len(args) == 1
        self.start_button = self.category = args[0]
        self.name = f"{self.name}/{self.category}"
        self.reload_items()

    def get_message(self) -> str:
        return super().get_message().replace("{{CATEGORY}}", self.category)

    def get_buttons(self) -> ReplyMarkupType:
        if self.selected_article:
            return get_keyboard_for_article(self.selected_article)
        return super().get_buttons()

    def mark_as_read(self, article: Article) -> None:
        article.view(self.user.id)
        self.selected_article = article


class ArticleState(BaseState):
    name = "Articles"

    selected_article: Article | None

    def __init__(self, user: User, text: str) -> None:
        self.selected_article = None
        super().__init__(user, text)

        assert self.buttons
        self.buttons = [[e] for e in list_categories()] + [[flatten(self.buttons)[-1]]]

        self.transitions = self.transitions.copy()
        for e in list_categories():
            self.transitions[e] = f"{ArticleCategoryState.name}/{e}"

    def action(self, action: str, pram: int) -> None:
        if action == "like":
            delta = 1
        elif action == "dislike":
            delta = -1
        else:
            return super().action(action, pram)

        article = get_article(pram)
        article.like(delta, self.user.id)
        self.message = ""
        self.selected_article = article

    def get_buttons(self) -> ReplyMarkupType:
        if self.selected_article:
            return get_keyboard_for_article(self.selected_article)
        return super().get_buttons()
