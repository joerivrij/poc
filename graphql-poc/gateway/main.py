from common import schemas
from . import backends
import graphene
from fastapi import FastAPI
from graphene import ObjectType, String, List, Field, Int
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


class Query(ObjectType):
    get_all_movies = Field(schemas.MovieListGq)
    get_all_books = List(schemas.BooksGraphql)
    get_all_authors = List(schemas.AuthorGraphql)
    get_movies = Field(List(schemas.MoviesGraphql), title=String())
    get_author_tree = Field(schemas.AuthorBooks, id=String())
    get_complete_tree = Field(schemas.CombinedTree, id=String(), year=Int())

    async def resolve_get_all_movies(self, info):
        movies = backends.get_movies()
        d = schemas.MovieListGq
        d.movies = movies
        return d

    async def resolve_get_all_books(self, info):
        books = backends.get_books()
        return books

    async def resolve_get_all_authors(self, info):
        authors = backends.get_authors()
        return authors

    async def resolve_get_author_tree(self, info, id):
        author = backends.get_author(id=id)
        books = backends.get_books_by_author(author_id=author["id"])
        resp = schemas.AuthorBooks
        resp.id = author["id"]
        resp.name = author["first_name"] + " " + author["last_name"]
        resp.date_of_birth = author["date_of_birth"]
        resp.books = books
        return resp

    async def resolve_get_movies(self, info, title):
        movies = backends.get_movies()
        if title == "":
            return movies
        m = []
        for movie in movies:
            if movie["title"] == title:
                m.append(movie)
        return m

    async def resolve_get_complete_tree(self, info, id):
        resp = schemas.CombinedTree
        author = backends.get_author(id=id)
        books = backends.get_books_by_author(author_id=author["id"])
        auth = schemas.AuthorBooks
        auth.id = author["id"]
        auth.name = author["first_name"] + " " + author["last_name"]
        auth.date_of_birth = author["date_of_birth"]
        auth.books = books
        movies = []
        for book in books:
            filtered_movies = backends.get_movies_with_filter(
                filter_look_up=book["title"]
            )
            for m in filtered_movies:
                movie = schemas.MovieData.from_dict(m)
                movies.append(movie)
        resp.author = auth
        resp.movies = movies
        return resp


app = FastAPI(
    title="Movies and More!", description="GraphQL Example App", version="0.1"
)


@app.get("/")
async def root():
    return {"message": "Contact Applications!"}


schema = graphene.Schema(query=Query)

app.mount("/graphql", GraphQLApp(schema, on_get=make_graphiql_handler()))
