from ..database import Base, engine
from .ActionLog import ActionLog
from .User import User

__all__ = ["ActionLog", "User"]

Base.metadata.create_all(engine)
