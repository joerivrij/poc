import logging

from fastapi import Depends, FastAPI, HTTPException
from fastapi.logger import logger
from sqlalchemy.orm import Session
from . import models, repo, validator
from .database import SessionLocal, engine
from common.schemas import sql as schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    return db


@app.get("/books")
async def books(db: Session = Depends(get_db)):
    books = repo.get_books(db=db)
    logger.log(msg=books, level=logging.INFO)
    return books


@app.get("/books/{author_id}")
async def root(author_id: int, db: Session = Depends(get_db)):
    books = repo.get_books_by_author(db=db, author_id=author_id)
    return books


@app.post("/books", status_code=201)
def create_new_book(book: schemas.Book, db: Session = Depends(get_db)):
    return repo.create_book(db=db, book=book)


@app.post("/books/{author_id}", status_code=201)
def create_new_book(
    book: schemas.BookCreate, author_id: str, db: Session = Depends(get_db)
):
    return repo.create_book_with_id(db=db, book=book, author_id=author_id)
