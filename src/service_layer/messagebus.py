from typing import List, Dict, Callable, Type
from src.domain import events
from src.service_layer import unit_of_work, services


def handle(event: events.Event, uow: unit_of_work.AbstractMemberUnitOfWork):
    for handler in HANDLERS[type(event)]:
        if uow:
            handler(event, uow)
        else:
            handler(event)


def update_member_books_after_borrow(event: events.UpdateMemberBooksAfterBorrow,
                                     uow: unit_of_work.AbstractMemberUnitOfWork):
    services.update_member_books(event.borrower_id, event.book_id, uow)


HANDLERS = {
    events.UpdateMemberBooksAfterBorrow: [update_member_books_after_borrow]
}  # type: Dict[Type[events.Event], List[Callable]]
