from quizlib.models import ActionLog, Article, Quiz, QuizResult, Recommendation, Technique

from ..database import Base, engine
from .QuizAnswer import QuizAnswer
from .User import User

__all__ = [
    "ActionLog",
    "User",
    "Article",
    "Quiz",
    "Technique",
    "QuizAnswer",
    "QuizResult",
    "Recommendation",
]

Base.metadata.create_all(engine)
