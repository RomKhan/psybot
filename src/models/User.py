from sqlalchemy import Column, Integer, String

from ..database import Base, TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = "telegram_users"
    message_unix_time = Column(Integer, nullable=False)
    state_name = Column(String(255), nullable=False)
    page_number = Column(Integer, nullable=True)
