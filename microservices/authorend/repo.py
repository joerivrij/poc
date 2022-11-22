from uuid import uuid4

from sqlalchemy.orm import Session

from . import models
from common.schemas import sql as schemas


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: str):
    return db.query(models.Author).filter(models.Author.uuid == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate):
    uuid = str(uuid4())
    db_author = models.Author(**author.dict(), uuid=uuid)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author: schemas.Author):
    db.delete(author)
    db.commit()
