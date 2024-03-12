from functools import lru_cache

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from quizlib.api import grade_quiz

from ..database import session
from ..models import Quiz, QuizAnswer
from ..util import ReplyMarkupType
from .BaseState import BaseState
from quizlib.util import to_english_category_name


@lru_cache
def get_quiz(id: int) -> Quiz:
    # todo: cache questions and answers
    return session.query(Quiz).get(id)


class QuizState(BaseState):
    name = "Quiz"
    quiz: Quiz
    question_index: int
    num_questions: int
    ans: QuizAnswer | None
    inline_answers: bool
    random_button = None

    def set_substate(self, *args: str) -> None:
        assert len(args) == 2
        self.quiz = get_quiz(int(args[0]))
        self.question_index = int(args[1])
        self.num_questions = max(len(self.quiz.questions), len(self.quiz.answers))  # type: ignore
        self.name = f"{self.name}/{self.quiz.id}/{self.question_index}"
        self.ans = self.get_quizans()
        self.inline_answers = any(len(ans) > 21 for ans in self.get_answers())

    def get_quizans(self, delta: int = 0) -> QuizAnswer | None:
        return session.query(QuizAnswer).filter_by(**self.get_quizans_id(delta)).one_or_none()

    def get_quizans_id(self, delta: int = 0) -> dict:
        ind = self.question_index + delta
        return dict(user_id=self.user.id, quiz_id=self.quiz.id, question_index=ind)

    def get_message(self) -> str:
        if self.question_index == self.num_questions:
            return "Вопросов больше нет, идём домой ребятки 0_0"
        elif self.question_index > self.num_questions:
            return super().get_message()

        res = super().get_message()
        res = res.replace("{{INDEX}}", str(self.question_index + 1))
        res = res.replace("{{TOTAL}}", str(self.num_questions))
        res = res.replace("{{NAME}}", str(self.quiz.name))
        res += f"\n\n{self.get_question()}"

        if self.inline_answers:
            res += "\n\nВарианты ответов:"
            for i, ans in enumerate(self.get_answers()):
                res += f"\n{i+1}. {ans}"

        if self.ans:
            res += f"\n\nРанее сохранённый ответ «{self.ans.ans_string()}»"
        return res

    def get_answers(self) -> list[str]:
        arr: list[list[str]] = self.quiz.answers  # type: ignore
        return arr[self.question_index % len(arr)]

    def get_question(self) -> str:
        arr: list[str] = self.quiz.questions  # type: ignore
        return arr[self.question_index % len(arr)]

    def get_buttons(self) -> ReplyMarkupType:
        row_width = 7 if self.inline_answers else 2
        res = InlineKeyboardMarkup(row_width=row_width)
        name = f"{self.__class__.name}/{self.quiz.id}"

        if self.question_index == self.num_questions:
            action = f"{name}/{self.question_index+1}/end:0"  # todo: different state?
            res.add(InlineKeyboardButton(text=self.buttons[-1][2], callback_data=action))
        elif self.question_index >= self.num_questions:
            return None
        else:
            for i, ans in enumerate(self.get_answers()):
                action = f"{name}/{self.question_index+1}/answer:{i}"
                text = str(i + 1) if self.inline_answers else ans
                res.insert(InlineKeyboardButton(text=text, callback_data=action))

        if self.question_index:
            action = f"{name}/{self.question_index-1}/goto:0"
            res.add(InlineKeyboardButton(text=self.buttons[-1][0], callback_data=action))
        else:
            action = f"QuizCategory/{self.quiz.category[:20]}/show:{self.quiz.id}"
            res.add(InlineKeyboardButton(text=self.buttons[-1][1], callback_data=action))

        return res

    def save_answer(self, answer_index: int) -> None:
        ans = self.get_quizans(-1)
        if ans:
            ans.answer_index = answer_index  # type: ignore
        else:
            session.add(QuizAnswer(**self.get_quizans_id(-1), answer_index=answer_index))

    def action(self, action: str, pram: int) -> None:
        if action == "goto" or action == "start":
            pass
        elif action == "answer":
            self.save_answer(pram)
        elif action == "end":
            answers = (
                session.query(QuizAnswer)
                .filter_by(user_id=self.user.id, quiz_id=self.quiz.id)
                .order_by(QuizAnswer.question_index)
                .all()
            )
            strings = [ans.ans_string() for ans in answers]
            res = grade_quiz(self.quiz.id, self.user.id, strings)  # type: ignore
            self.message = res.content  # type: ignore
        else:
            return super().action(action, pram)