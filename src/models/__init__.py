from ..database import Base, engine
from .ActionLog import ActionLog
from .Article import Article
from .User import User

__all__ = ["ActionLog", "User", "Article"]

Base.metadata.create_all(engine)
