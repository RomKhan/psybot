from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from environment import DATABASE_URI

Base = declarative_base()
engine = create_engine(DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
