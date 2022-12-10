from functools import lru_cache
from typing import Collection

from ..database import session
from ..models import Article, Technique, User
from ..util import ReplyMarkupType
from .LikeableState import LikeableState
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


class ArticleCategoryState(PageableState):
    category: str
    name = "ArticleCategory"
    random_button = "Случайная статья"
    start_button = ""
    is_random = False
    item_name = "Статья"

    items: list[tuple[int, str]]
    selected_article: Article | Technique | None

    def get_items(self) -> list[tuple[int, str]]:
        return articles_by_cat(self.category, self.user.is_subscribed())

    def get_headline(self, article: tuple[int, str]) -> str:
        return article[1]

    def get_article(self) -> Article | Technique:
        return get_article(self.items[self.item_number][0])

    def print_item(self) -> str:
        article = self.get_article()
        self.mark_as_read(article)
        text = " ".join(article.content.split()[:50])
        res = [
            f"{self.item_name} №{self.item_number+1} в категории «{self.category}»",
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
        # todo: use both keyboards
        if self.selected_article:
            return ArticleState.likes_keyboard(self.selected_article)
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
