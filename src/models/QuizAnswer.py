from quizlib.models import Quiz
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from ..database import Base, TimestampMixin
from ..models import User


class QuizAnswer(TimestampMixin, Base):
    __tablename__ = "quiz_answers"

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    quiz_id = Column(Integer, ForeignKey(Quiz.id), nullable=False)

    question_index = Column(Integer, nullable=False)
    answer_index = Column(Integer, nullable=False)

    quiz = relationship(Quiz, uselist=False)
    user = relationship(User, uselist=False)

    __table_args__ = (UniqueConstraint("user_id", "quiz_id", "question_index"),)

    def ans_string(self) -> str:
        arr: list[list[str]] = self.quiz.answers
        return arr[self.question_index % len(arr)][self.answer_index]
