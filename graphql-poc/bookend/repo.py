from sqlalchemy.orm import Session

from . import models
from common import schemas


def get_books_by_author(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def create_author(db: Session, author: schemas.AuthorCreate, full_name: str):
    db_author = models.Author(**author.dict())
    db_author.full_name = full_name
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def create_book(db: Session, book: schemas.BookCreate, author_id: int):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book_bulk(db: Session, books: list[schemas.BookBulkCreate]):
    for book in books:
        db_book = models.Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    return
