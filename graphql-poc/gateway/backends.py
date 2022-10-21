import requests

BOOKEND_URL = "http://127.0.0.1:5002"
MOVIEND_URL = "http://127.0.0.1:5001"


def get_movies():
    url = MOVIEND_URL + "/movies"
    r = requests.get(url)
    movies = r.json()
    return movies


def get_movies_by_year(year):
    url = MOVIEND_URL + "/movies/" + str(year)
    r = requests.get(url)
    movies = r.json()
    return movies


def get_movies_with_filter(filter_look_up: str):
    words = filter_look_up.split(" ")
    look_up = "&look_up="
    for i, word in enumerate(words):
        if i == 0:
            look_up += word.lower()
        else:
            look_up += "%" + word.lower()
    url = MOVIEND_URL + "/movies" + look_up
    r = requests.get(url)
    movies = r.json()
    return movies


def get_books():
    url = BOOKEND_URL + "/books"
    r = requests.get(url)
    books = r.json()
    return books


def get_authors():
    url = BOOKEND_URL + "/authors"
    r = requests.get(url)
    authors = r.json()
    return authors


def get_author(id):
    url = BOOKEND_URL + "/authors/" + id
    r = requests.get(url)
    author = r.json()
    return author


def get_books_by_author(author_id):
    url = BOOKEND_URL + "/books/" + str(author_id)
    r = requests.get(url)
    books = r.json()
    return books


def get_movie(filter):
    url = MOVIEND_URL + "/movies"
    r = requests.get(url)
    movies = r.json()
    return movies
