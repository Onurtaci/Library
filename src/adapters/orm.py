from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import registry, relationship

from src.domain import model

metadata = MetaData()
mapper_registry = registry()

books = Table(
    "books",
    metadata,
    Column("book_id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255)),
    Column("author_names", String(255)),
    Column("physical_location", String(255)),
    Column("is_borrowed", Integer, default=0),  # 0 means not borrowed, 1 means borrowed
    Column("member_id", ForeignKey("members.member_id"), default=-1)
)

members = Table(
    "members",
    metadata,
    Column("member_id", Integer, primary_key=True, autoincrement=True),
    Column("first_name", String(255)),
    Column("last_name", String(255)),
    Column("phone_number", String(255)),
    Column("address", String(255)),
)

member_books = Table(
    "member_books",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("member_id", ForeignKey("members.member_id"), nullable=False),
    Column("book_id", ForeignKey("books.book_id"), nullable=False),
    Column("borrow_date", DateTime),
    Column("return_date", DateTime),
)


def start_mappers():
    mapper_registry.map_imperatively(model.Book, books)
    mapper_registry.map_imperatively(model.Member, members,
                                     properties={
                                         "_member_books": relationship(
                                             books,
                                             secondary=member_books,
                                             collection_class=set
                                         )
                                     })
