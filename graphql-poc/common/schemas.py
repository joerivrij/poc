from pydantic import BaseModel
from dataclasses import dataclass
from typing import Any, TypeVar, Type
from graphene import String, ObjectType, List, Field

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class MovieData:
    title: str
    year: int
    id: int
    imdb: str
    image: str
    description: str
    type: str

    @staticmethod
    def from_dict(obj: Any) -> "MovieData":
        assert isinstance(obj, dict)
        title = from_str(obj.get("title"))
        year = from_int(obj.get("year"))
        id = from_int(obj.get("id"))
        imdb = from_str(obj.get("imdb"))
        image = from_str(obj.get("image"))
        description = from_str(obj.get("description"))
        type = from_str(obj.get("type"))
        return MovieData(title, year, id, imdb, image, description, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["year"] = from_int(self.year)
        result["id"] = from_int(self.id)
        result["imdb"] = from_str(self.imdb)
        result["image"] = from_str(self.image)
        result["description"] = from_str(self.description)
        result["type"] = from_str(self.type)
        return result


class MovieBase(BaseModel):
    title: str
    year: int
    imdb: str
    type: str
    image: str
    description: str


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True

    @staticmethod
    def from_dict(obj: Any) -> "Movie":
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        title = from_str(obj.get("title"))
        year = from_int(obj.get("year"))
        imdb = from_str(obj.get("imdb"))
        image = from_str(obj.get("image"))
        description = from_str(obj.get("description"))
        type = from_str(obj.get("type"))
        return Movie(
            id=id,
            title=title,
            year=year,
            imdb=imdb,
            image=image,
            description=description,
            type=type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["year"] = from_int(self.year)
        result["imdb"] = from_str(self.imdb)
        result["image"] = from_str(self.image)
        result["description"] = from_str(self.description)
        result["type"] = from_str(self.type)
        result["id"] = from_int(self.id)
        return result


class BookBase(BaseModel):
    title: str
    publishing_year: str


class BookCreate(BookBase):
    pass


class BookBulkCreate(BookBase):
    author_id: int


class Book(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True


class AuthorBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    full_name: str
    items: list[Book] = []

    class Config:
        orm_mode = True


class MoviesGraphql(ObjectType):
    id = String()
    title = String(required=True)
    year = String()
    imdb = String()
    type = String()
    image = String()
    description = String()


class MovieListGq(ObjectType):
    movies = List(MoviesGraphql)


class BooksGraphql(ObjectType):
    id = String()
    title = String(required=True)
    publishing_year = String()


class AuthorGraphql(ObjectType):
    id = String()
    first_name = String()
    last_name = String()
    date_of_birth = String()


class AuthorBooks(ObjectType):
    id = String()
    name = String()
    date_of_birth = String()
    books = List(BooksGraphql)


class CombinedTree(ObjectType):
    author = Field(AuthorBooks)
    movies = List(MoviesGraphql)
