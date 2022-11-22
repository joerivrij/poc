from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, String
from .database import Base


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    author_id = Column(String)
    title = Column(String)
    publishing_year = Column(Integer)
