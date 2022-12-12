from functools import lru_cache
from typing import Collection

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from quizlib.util import humanize_category_name

from ..database import session
from ..models import Quiz
from ..util import ReplyMarkupType
from .CategoryState import CategoryState
from .LikeableState import BaseModel, LikeableState
from .QuizState import QuizState


@lru_cache
def list_quizzes() -> list[tuple[int, str, str, bool]]:
    columns = [Quiz.id, Quiz.category, Quiz.name, Quiz.needs_subscription]
    return session.query(*columns).distinct().all()


@lru_cache
def list_categories() -> Collection[str]:
    return set(e[1] for e in list_quizzes())


@lru_cache
def quizzes_by_cat(category: str, subscription: bool = False) -> list[tuple[int, str]]:
    return [
        (id, title)
        for id, cat, title, sub in list_quizzes()
        if cat == category and (subscription or not sub)
    ]


@lru_cache
def get_quiz(id: int) -> Quiz:
    return session.query(Quiz).get(id)


class QuizCategoryState(CategoryState):
    name = "QuizCategory"
    random_button = "Случайный тест"
    item_name = "Тест"

    selected_quiz: Quiz | None = None

    def get_message(self) -> str:
        category = humanize_category_name(self.category)
        return super().get_message().replace(self.category, category)

    def get_items(self) -> list[tuple[int, str]]:
        return quizzes_by_cat(self.category, self.user.is_subscribed())

    def print_item(self) -> str:
        quiz = get_quiz(self.items[self.item_number][0])
        self.selected_quiz = quiz
        category = humanize_category_name(self.category)
        res = [
            f"{self.item_name} №{self.item_number+1} в категории «{category}»",
            quiz.name,
            quiz.description,
            f"Затрата времени: {quiz.time} минут",
        ]
        return "\n\n".join(res)

    def get_buttons(self) -> ReplyMarkupType:
        # todo: use both keyboards
        if self.selected_quiz:
            return QuizzesState.likes_keyboard(self.selected_quiz)
        return super().get_buttons()

    def action(self, action: str, pram: int) -> None:
        if action == "show":
            self.item_number = next(i for i, (id, _) in enumerate(self.items) if id == pram)
            self.text = str(self.item_number + 1)
            self.message = self.compute_message()
        else:
            return super().action(action, pram)


class QuizzesState(LikeableState):
    name = "Quizzes"
    substate = QuizCategoryState

    def list_categories(self) -> Collection[str]:
        return list_categories()

    def get_item(self, id: int) -> Quiz:
        return get_quiz(id)

    def get_buttons(self) -> ReplyMarkupType:
        if self.selected_item:
            return self.likes_keyboard(self.selected_item)

        res = InlineKeyboardMarkup(row_width=1)
        for cat in self.list_categories():
            res.insert(InlineKeyboardButton(text=humanize_category_name(cat), callback_data=cat))
        res.add(InlineKeyboardButton(text=self.buttons[-1][0], callback_data=self.buttons[-1][0]))

        return res

    @classmethod
    def likes_keyboard(cls, item: BaseModel) -> InlineKeyboardMarkup:
        res = super(QuizzesState, cls).likes_keyboard(item)
        action = f"{QuizState.name}/{item.id}/0/start:0"
        res.row(InlineKeyboardButton(text="Начать", callback_data=action))
        return res
