from sqlalchemy import Column, Integer, String

from ..database import Base, TimestampMixin


class ActionLog(TimestampMixin, Base):
    __tablename__ = "action_log"
    user_id = Column(Integer, nullable=False)
    message_unix_time = Column(Integer, nullable=False)
    old_state_name = Column(String(255), nullable=False)
    new_state_name = Column(String(255), nullable=False)
    button_text = Column(String(255), nullable=False)
