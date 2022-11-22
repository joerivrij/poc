from graphene import String, ObjectType, List, Field


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
