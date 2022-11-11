import logging

from sqlalchemy import Column, DateTime, Integer, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

from .environment import DATABASE_URI, ECHO_SQL

if ECHO_SQL:
    logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

Base = declarative_base()
engine = create_engine(url=DATABASE_URI, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class TimestampMixin:
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
