from sqlalchemy.orm import Session

from . import models
from common.schemas import sql as schemas


def get_books_by_author(db: Session, author_id: int):
    return db.query(models.Book).filter(models.Book.author_id == author_id).all()


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def delete_book(db: Session, book: schemas.Book):
    db.delete(book)
    db.commit()


def create_book_with_id(db: Session, book: schemas.BookCreate, author_id: str):
    db_book = models.Book(**book.dict(), author_id=author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book(db: Session, book: schemas.Book):
    db_book = models.Book(**book.dict())
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


def create_book_bulk_json(db: Session, books):
    for book in books:
        db_book = models.Book(**book)
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    return
