from typing import Any

from sqlalchemy import Boolean, Column, Date, Integer, String, Text, UniqueConstraint

from ..database import Base, TimestampMixin


class Article(TimestampMixin, Base):
    __tablename__ = "data_articles"

    author = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    category = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    needs_subscription = Column(Boolean, nullable=False, default=False)

    date = Column(Date, nullable=False)
    reading_time = Column(Integer, nullable=False)
    article_url = Column(String(255), nullable=False, unique=True)
    image_url = Column(String(255), nullable=True)

    likes = Column(Integer, nullable=False, default=0)
    views = Column(Integer, nullable=False, default=0)

    __table_args__ = (UniqueConstraint("title", "category"),)

    def to_dict(self) -> dict[str, Any]:
        return {
            "author": self.author,
            "title": self.title,
            "category": self.category,
            "content": self.content,
            "needs_subscription": self.needs_subscription,
            "date": str(self.date),
            "reading_time": self.reading_time,
            "article_url": self.article_url,
            "image_url": self.image_url,
            "likes": self.likes,
            "views": self.views,
        }
