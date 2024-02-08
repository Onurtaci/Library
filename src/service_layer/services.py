from src.domain import model, events
from src.service_layer import unit_of_work, messagebus


def add_book(book_id: int, title: str, author_names: str, physical_location: str,
             uow: unit_of_work.AbstractBookUnitOfWork):
    with uow:
        book = uow.books.get(book_id)
        if book is None:
            book = model.Book(book_id=book_id, title=title, author_names=author_names,
                              physical_location=physical_location)
            uow.books.add(book)
        else:
            raise "Book already exists"
        uow.commit()


def add_member(member_id: int, first_name: str, last_name: str, phone_number: str, address: str,
               uow: unit_of_work.AbstractMemberUnitOfWork):
    with uow:
        member = uow.members.get(member_id)
        if member is None:
            member = model.Member(member_id=member_id, first_name=first_name, last_name=last_name,
                                  phone_number=phone_number, address=address)
            uow.members.add(member)
        else:
            raise "Member already exists"
        uow.commit()


def borrow_book(book_id: int, member_id, uow: unit_of_work.AbstractBookUnitOfWork,
                member_uow: unit_of_work.AbstractMemberUnitOfWork):
    with uow:
        book = uow.books.get(book_id)
        if book is None:
            raise ValueError("Book not found")
        book.borrow_book(member_id)
        uow.commit()
        event = events.UpdateMemberBooksAfterBorrow(member_id, book_id)
        messagebus.handle(event, member_uow)


def update_member_books(borrower_id: int, book_id: int, uow: unit_of_work.AbstractMemberUnitOfWork):
    with uow:
        member = uow.members.get(borrower_id)
        if member is None:
            raise ValueError("Member not found")
        member.borrowed_books.add(book_id)
        uow.commit()
