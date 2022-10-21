import logging

from fastapi import Depends, FastAPI
from fastapi.logger import logger
from sqlalchemy.orm import Session
from . import repo, models
from .database import SessionLocal, engine
from common import schemas

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


@app.post("/booksBulk")
async def root(books: list[schemas.BookBulkCreate], db: Session = Depends(get_db)):
    repo.create_book_bulk(db=db, books=books)
    return {"success": True}


@app.post("/books/{author_id}", response_model=schemas.BookCreate)
def create_new_book(
    book: schemas.BookCreate, author_id: int, db: Session = Depends(get_db)
):
    return repo.create_book(db=db, book=book, author_id=author_id)


@app.get("/authors")
async def fetch_authors(db: Session = Depends(get_db)):
    authors = repo.get_authors(db=db)
    print(authors)
    return authors


@app.get("/authors/{author_id}")
async def fetch_authors(author_id: int, db: Session = Depends(get_db)):
    author = repo.get_author(db=db, author_id=author_id)
    return author


@app.post("/authors", response_model=schemas.AuthorCreate)
def create_new_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    full_name = author.first_name + " " + author.last_name
    author.full_name = full_name
    return repo.create_author(db=db, author=author)


@app.post("/authorsBulk")
def create_new_author(
    authors: list[schemas.AuthorCreate], db: Session = Depends(get_db)
):
    for author in authors:
        full_name = author.first_name + " " + author.last_name
        repo.create_author(db=db, author=author, full_name=full_name)
    return {"success": True}
