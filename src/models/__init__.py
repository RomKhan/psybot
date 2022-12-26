from quizlib.models import ActionLog, Article, Quiz, QuizResult, Technique

from ..database import Base, engine
from .QuizAnswer import QuizAnswer
from .User import User

__all__ = ["ActionLog", "User", "Article", "Quiz", "Technique", "QuizAnswer", "QuizResult"]

Base.metadata.create_all(engine)
