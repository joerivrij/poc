from common import schemas
from . import repo


BLOCK_LIST = ["war", "shit"]


def validate_movie(movie, db):
    for word in BLOCK_LIST:
        if word in movie.title.lower():
            return {
                "valid": False,
                "reason": "the movie title contains a word from the block_list",
            }

    unique = repo.get_movie_by_imdb(db, movie.imdb)
    if unique is not None:
        return {
            "valid": False,
            "reason": "the imdb id is already present in the database",
        }

    return {"valid": True, "reason": "this is a valid movie"}
