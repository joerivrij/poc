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


@app.get("/authors")
async def fetch_authors(db: Session = Depends(get_db)):
    authors = repo.get_authors(db=db)
    print(authors)
    return authors


@app.get("/authors/{author_id}")
async def fetch_authors(author_id: str, db: Session = Depends(get_db)):
    author = repo.get_author(db=db, author_id=author_id)
    return author


@app.post("/authorsBulk")
def create_new_author(
    authors: list[schemas.AuthorCreate], db: Session = Depends(get_db)
):
    for author in authors:
        valid = validator.validate_author(author)
        if not valid["valid"]:
            raise HTTPException(status_code=400, detail=valid)
        full_name = author.first_name + " " + author.last_name
        author.full_name = full_name
        repo.create_author(db=db, author=author)
    return {"success": True}


@app.post("/authors", status_code=201)
async def create_new_author(
    author: schemas.AuthorCreate, db: Session = Depends(get_db)
):
    valid = validator.validate_author(author)
    if not valid["valid"]:
        raise HTTPException(status_code=400, detail=valid)

    return repo.create_author(db=db, author=author)


@app.delete("/authors/{author_id}", status_code=204)
async def create_new_author(author_id: str, db: Session = Depends(get_db)):
    author = repo.get_author(db, author_id=author_id)
    repo.delete_author(db, author)
    return
