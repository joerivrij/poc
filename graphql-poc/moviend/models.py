from sqlalchemy import Column, Integer, String
from .database import Base


class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    imdb = Column(String)
    type = Column(String)
    image = Column(String)
    description = Column(String)
