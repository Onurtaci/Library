from flask import Flask, request

from src.adapters import orm
from src.service_layer import services, unit_of_work

app = Flask(__name__)
orm.start_mappers()


@app.route("/add_book", methods=["POST"])
def add_book():
    services.add_book(
        request.json["book_id"],
        request.json["title"],
        request.json["author_names"],
        request.json["physical_location"],
        unit_of_work.SqlAlchemyBookUnitOfWork()
    )
    return "OK", 201


@app.route("/add_member", methods=["POST"])
def add_member():
    services.add_member(
        request.json["member_id"],
        request.json["first_name"],
        request.json["last_name"],
        request.json["phone_number"],
        request.json["address"],
        unit_of_work.SqlAlchemyMemberUnitOfWork()
    )
    return "OK", 201


@app.route("/borrow_book", methods=["POST"])
def borrow_book():
    services.borrow_book(
        request.json["book_id"],
        request.json["member_id"],
        unit_of_work.SqlAlchemyBookUnitOfWork(),
        unit_of_work.AbstractMemberUnitOfWork()
    )
    return "OK", 201
