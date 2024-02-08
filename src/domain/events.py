from dataclasses import dataclass


class Event:
    pass


@dataclass
class UpdateMemberBooksAfterBorrow(Event):
    def __init__(self, borrower_id: int, book_id: int):
        self.borrower_id = borrower_id
        self.book_id = book_id
