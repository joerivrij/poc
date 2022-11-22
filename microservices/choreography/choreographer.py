import json
import time
from uuid import uuid4

import pika.exceptions
from common.backend import services
from common.schemas import sql


queue_name = "choreography"
param = pika.ConnectionParameters(host="localhost", port=5672)
connection = pika.BlockingConnection(param)
channel = connection.channel()
channel.queue_declare(queue=queue_name)


def publish(body):
    channel.basic_publish(exchange="", routing_key=queue_name, body=body)


def consume():
    method_frame, header_frame, body = channel.basic_get(queue_name)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    return body


def create_saga(tree):
    print("starting choreograph")
    create_author = services.create_author(tree['author'])
    if create_author.status_code == 201:
        print("created author")
        books = json.dumps(tree['books'], indent=2).encode('utf-8')
        publish(books)
    else:
        print(create_author.json())
        print("failed to create author")
        return

    print("short break")
    time.sleep(1)
    author_id = create_author.json()["uuid"]

    book_message = consume()

    books = json.loads(book_message)
    print(books)
    for book in books:
        book_body = sql.Book(
            title=book['title'], publishing_year=book['publishing_year'], author_id=author_id
        )

        json_book = json.loads(book_body.json())
        create_books = services.create_books(json_book)
        print("book created")
        print(create_books.json())
        if create_books.status_code != 201:
            return

    print("putting movies on queue")
    movies = json.dumps(tree['movies'], indent=2).encode('utf-8')
    publish(movies)
    print("short break")
    time.sleep(1)

    movie_message = consume()

    movies = json.loads(movie_message)
    print(movies)

    for movie in movies:
        create_movie = services.create_movie(movie)
        if create_movie.status_code == 201:
            print("created movie")
        else:
            print("failed to create movie")
            return


def start_saga():
    imdb = str(uuid4())
    tree = '''
    {
  "author": {
    "first_name": "Mark",
    "last_name": "Twain",
    "date_of_birth": "30-11-1835"
  },
  "books": [
    {
      "title": "Huckleberry Finn",
      "publishing_year": 1865
    }
  ],
  "movies": [
    {
      "title": "Once Upon a Time in the West",
      "year": 1968,
      "imdb": "tt0064116",
      "image": "https://m.media-amazon.com/images/M/MV5BZGI5MjBmYzYtMzJhZi00NGI1LTk3MzItYjBjMzcxM2U3MDdiXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_SY1000_CR0,0,658,1000_AL_.jpg",
      "description": "Whatever you read here is untrue",
      "type": "movie"
    }
  ]
}
    '''

    data = json.loads(tree)
    data['movies'][0]['imdb'] = imdb
    create_saga(tree=data)


if __name__ == "__main__":
    start_saga()
