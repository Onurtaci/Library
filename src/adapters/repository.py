import abc
from typing import Set

from src.domain import model


class AbstractBookRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Book]

    def add(self, book: model.Book):
        self._add(book)
        self.seen.add(book)

    def get(self, book_id: int) -> model.Book:
        book = self._get(book_id)
        if book:
            self.seen.add(book)
        return book

    @abc.abstractmethod
    def _add(self, book: model.Book):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, book_id) -> model.Book:
        raise NotImplementedError


class AbstractMemberRepository(abc.ABC):
    def __init__(self):
        self.seen = set()  # type: Set[model.Member]

    def add(self, member: model):
        self._add(member)
        self.seen.add(member)

    def get(self, member_id: int) -> model.Member:
        member = self._get(member_id)
        if member:
            self.seen.add(member)
        return member

    @abc.abstractmethod
    def _add(self, member: model.Member) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, member_id: int) -> model.Member:
        raise NotImplementedError


class SqlAlchemyBookRepository(AbstractBookRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, book: model.Book):
        self.session.add(book)

    def _get(self, book_id: int) -> model.Book:
        return self.session.query(model.Book).filter_by(book_id=book_id).first()


class SqlAlchemyMemberRepository(AbstractMemberRepository):
    def __init__(self, session):
        super().__init__()
        self.session = session

    def _add(self, member: model.Member):
        self.session.add(member)

    def _get(self, member_id: int) -> model.Member:
        return self.session.query(model.Member).filter_by(member_id=member_id).first()
