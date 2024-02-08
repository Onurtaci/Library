from datetime import datetime
from typing import Set, List

from src.domain import events


class Book:
    def __init__(self, book_id: int, title: str, author_names: str, physical_location: str):
        self.book_id = book_id
        self.title = title
        self.author_names = author_names
        self.physical_location = physical_location
        self.borrower_id = None
        self.is_borrowed = False
        self.borrow_date = None
        self.due_date = None
        self.events = []  # type: List[events.Event]

    def borrow_book(self, member_id: int) -> int:
        if self.can_borrow():
            self.is_borrowed = True
            self.borrower_id = member_id
            self.borrow_date = datetime.now()
            self.due_date = None
            self.events.append(events.UpdateMemberBooksAfterBorrow(self.borrower_id, self.book_id))
            return self.book_id
        else:
            raise "The book is already borrowed"

    def can_borrow(self) -> bool:
        return not self.is_borrowed


class Member:
    def __init__(self, member_id: int, first_name: str, last_name: str, phone_number: str, address: str):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.borrowed_books = set()  # type: Set[int]
