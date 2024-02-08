import pytest

from src.domain import model
from src.service_layer import services, unit_of_work
from src.adapters import repository


class FakeBookRepository(repository.AbstractBookRepository):
    def __init__(self, books):
        super().__init__()
        self._books = set(books)

    def _add(self, book):
        self._books.add(book)

    def _get(self, book_id):
        return next((p for p in self._books if p.book_id == book_id), None)


class FakeMemberRepository(repository.AbstractMemberRepository):
    def __init__(self, members):
        super().__init__()
        self._members = set(members)

    def _add(self, member):
        self._members.add(member)

    def _get(self, member_id):
        return next((p for p in self._members if p.member_id == member_id), None)


class FakeBookUnitOfWork(unit_of_work.AbstractBookUnitOfWork):
    def __init__(self):
        book = model.Book(1, "Python Programming", "Guido van Rossum", "Aisle 3, Shelf")
        self.books = FakeBookRepository([book])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


class FakeMemberUnitOfWork(unit_of_work.AbstractMemberUnitOfWork):
    def __init__(self):
        member = model.Member(1, "John", "Doe", "555-1234", "123 Main Street")
        self.members = FakeMemberRepository([member])
        self.committed = False

    def _commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_book():
    uow = FakeBookUnitOfWork()
    services.add_book(2, "Python Programming", "Guido van Rossum", "Aisle 3, Shelf 2", uow)
    assert uow.books.get(1).title == "Python Programming"


def test_add_member():
    uow = FakeMemberUnitOfWork()
    services.add_member(3, "John", "Doe", "555-1234", "123 Main Street", uow)
    assert uow.members.get(1).first_name == "John"


def test_borrow_book():
    uow = FakeBookUnitOfWork()
    member_uow = FakeMemberUnitOfWork()
    services.borrow_book(1, 1, uow, member_uow)
    assert uow.books.get(1).is_borrowed
