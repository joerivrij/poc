from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, ForeignKey, Integer, String
from .database import Base
from enum import Enum


class Saga(Base):
    __tablename__ = "saga"
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    status = Column(String)
    type = Column(String)
    reason = Column(String)


# class Fail(Base):
#     __tablename__ = "failures"
#     id = Column(Integer, primary_key=True)
#     saga_id = Column(String, foreign_key=())
#     reason = Column(String)


class Status(Enum):
    CREATED = 1
    PENDING = 2
    APPROVED = 3
    FAILED = 4


class SagaType(Enum):
    MOVIE = 1
    AUTHOR = 2
    BOOK = 3
    SAGA = 4
