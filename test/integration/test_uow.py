from test.confest import session_factory
from src.domain import model
from src.service_layer import unit_of_work


def insert_book(session, book_id, title, author_names, physical_location):
    session.execute(
        "INSERT INTO books VALUES (:book_id, :title, :author_names, :physical_location)",
        dict(book_id=book_id, title=title, author_names=author_names, physical_location=physical_location)
    )


def get_book_is_borrowed(session, book_id) -> int:
    [[is_borrowed]] = session.execute(
        "SELECT books.is_borrowed FROM books WHERE book_id = :book_id",
        dict(book_id=book_id)
    )
    return is_borrowed


def insert_member(session, member_id, first_name, last_name, phone_number, address):
    session.execute(
        "INSERT INTO members VALUES (:member_id, :first_name, :last_name, :phone_number, :address)",
        dict(member_id=member_id, first_name=first_name, last_name=last_name, phone_number=phone_number,
             address=address)
    )


def test_uow_can_borrow_book(session_factory):
    session = session_factory
    insert_book(session, "1", "Python Programming", "Guido van Rossum", "Aisle 3, Shelf 2")
    session.commit()

    uow = unit_of_work.SqlAlchemyBookUnitOfWork(session_factory)
    with uow:
        book = uow.books.get(book_id="1")
        member = model.Member(1, "John", "Doe", "555-1234", "123 Main Street")
        book.borrow_book(member.member_id)
        uow.commit()

    book_is_borrowed = get_book_is_borrowed(session, book_id="1")
    assert book_is_borrowed
