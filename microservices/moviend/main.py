from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/movies")
async def fetch_movies(db: Session = Depends(get_db)):
    return repo.get_movies(db=db)


@app.get("/movies/{year}")
async def fetch_movies_by_year(year: int, db: Session = Depends(get_db)):
    return repo.get_movie_by_year(db=db, year=year)


@app.get("/movies{look_up}")
async def fetch_movies_with_lookup(look_up: str, db: Session = Depends(get_db)):
    db_movies = repo.get_movies(db=db)
    filter_list = ["the", "and", "of", "a", "an", "&", "I"]
    movies = []
    look_up_words = look_up.split("=")[1].split("%")
    filtered_list = []
    for word in look_up_words:
        if word not in filter_list:
            filtered_list.append(word)
    for movie in db_movies:
        for word in filtered_list:
            if word.lower() in movie.title.lower():
                append = True
                if len(movies) > 0:
                    for found_movie in movies:
                        if movie.id is found_movie.id:
                            append = False
                if append:
                    movies.append(movie)
    return movies


@app.post("/movies", status_code=201)
def create_new_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    valid = validator.validate_movie(db=db, movie=movie)
    if not valid["valid"]:
        raise HTTPException(status_code=400, detail=valid)
    repo.create_movie(db=db, movie=movie)
    return {"success": True}


@app.post("/moviesBulk")
def create_new_author(movies: list[schemas.MovieCreate], db: Session = Depends(get_db)):
    for movie in movies:
        repo.create_movie(db=db, movie=movie)
    return {"success": True}
