from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, String
from .database import Base


class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    publishing_year = Column(Integer)
    author_id = Column(Integer, ForeignKey("author.id"))
    author = relationship("Author", back_populates="book")


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    date_of_birth = Column(String)
    book = relationship("Book", back_populates="author")
