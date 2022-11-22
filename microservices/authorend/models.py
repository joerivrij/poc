from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, String
from .database import Base


class Author(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
