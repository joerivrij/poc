import json
import time

from common.backend import services
from common.schemas import sql
from . import models, repo
from common.schemas import saga


async def create_saga(uuid, tree, db):
    print("starting")
    saga_type = models.SagaType
    status = models.Status
    saga_model = saga.SagaCreate(
        type=saga_type.SAGA.name,
        uuid=uuid,
        status=status.CREATED.name,
        reason=status.CREATED.name,
    )
    repo.create_saga(db, saga_data=saga_model)
    print("created saga")
    saga_model = saga.SagaCreate(
        type=saga_type.AUTHOR.name,
        uuid=uuid,
        status=status.PENDING.name,
        reason=status.PENDING.name,
    )
    repo.create_saga(db, saga_data=saga_model)

    print("pretending like it's a long call to the DB")
    for sec in range(1, 5):
        print("creating author")
        time.sleep(1)

    author = json.loads(tree.author.json())
    create_author = services.create_author(author)
    if create_author.status_code == 201:
        print("created author")
        saga_model = saga.SagaCreate(
            type=saga_type.AUTHOR.name,
            uuid=uuid,
            status=status.CREATED.name,
            reason=status.CREATED.name,
        )
        repo.create_saga(db, saga_data=saga_model)
    else:
        print("failed to create author")
        saga_model = saga.SagaCreate(
            type=saga_type.AUTHOR.name,
            uuid=uuid,
            status=status.FAILED.name,
            reason=create_author.json(),
        )
        repo.create_saga(db, saga_data=saga_model)

    saga_model = saga.SagaCreate(
        type=saga_type.BOOK.name,
        uuid=uuid,
        status=status.PENDING.name,
        reason=status.PENDING.name,
    )

    repo.create_saga(db, saga_data=saga_model)

    author_id = create_author.json()["uuid"]

    for book in tree.books:
        book_body = sql.Book(
            title=book.title, publishing_year=book.publishing_year, author_id=author_id
        )
        json_book = json.loads(book_body.json())
        create_books = services.create_books(json_book)
        if create_books.status_code == 201:
            print("created book")
            saga_model = saga.SagaCreate(
                type=saga_type.BOOK.name,
                uuid=uuid,
                status=status.CREATED.name,
                reason=status.CREATED.name,
            )
            repo.create_saga(db, saga_data=saga_model)
        else:
            print("failed to create book")
            saga_model = saga.SagaCreate(
                type=saga_type.BOOK.name,
                uuid=uuid,
                status=status.FAILED.name,
                reason=create_author.json(),
            )
            repo.create_saga(db, saga_data=saga_model)

        saga_model = saga.SagaCreate(
            type=saga_type.MOVIE.name,
            uuid=uuid,
            status=status.PENDING.name,
            reason=status.PENDING.name,
        )

    print("pretending like it's a long call to the DB")
    for sec in range(1, 4):
        print("creating book")
        time.sleep(1)

    repo.create_saga(db, saga_data=saga_model)
    for movie in tree.movies:
        print("pretending like it's a long call to the DB")
        for sec in range(1, 3):
            print("creating movie")
            time.sleep(1)
        json_movie = json.loads(movie.json())
        create_movie = services.create_movie(json_movie)
        if create_movie.status_code == 201:
            print("created movie")
            saga_model = saga.SagaCreate(
                type=saga_type.MOVIE.name,
                uuid=uuid,
                status=status.CREATED.name,
                reason=status.CREATED.name,
            )
            repo.create_saga(db, saga_data=saga_model)
        else:
            print("failed to create movie")
            r = create_movie.json()
            print(r)
            reason = r["detail"]["reason"]
            print(reason)
            saga_model = saga.SagaCreate(
                type=saga_type.MOVIE.name,
                uuid=uuid,
                status=status.FAILED.name,
                reason=reason,
            )
            repo.create_saga(db, saga_data=saga_model)
