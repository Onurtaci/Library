import requests
import pytest
from src import config
from test.confest import restart_api
from test.confest import postgres_db


def post_to_add_book(book_id, title, author_names, physical_location) -> int:
    url = config.get_api_url()
    r = requests.post(url, json={'book_id': book_id,
                                 'title': title,
                                 'author_names': author_names,
                                 'physical_location': physical_location})
    return r.status_code
    assert r.status_code == 201


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path_return_201():
    book_id = 12
    title = "Book Title"
    author_names = "Author1, Author2"
    physical_location = "Aisle 3, Shelf 6"
    status_code = post_to_add_book(book_id, title, author_names, physical_location)
    assert status_code == 201
