from flask import Blueprint
from service.bookService import BookService

def create_book_blueprint(mysql):
    book_routes = Blueprint("bookRoutes", __name__)
    book_service = BookService(mysql)

    book_routes.add_url_rule("/books", view_func=book_service.get_all, methods=["GET"])
    book_routes.add_url_rule("/books/<int:id>", view_func=book_service.get_by_id, methods=["GET"])
    book_routes.add_url_rule("/books", view_func=book_service.create, methods=["POST"])
    book_routes.add_url_rule("/books/<int:id>", view_func=book_service.update, methods=["PUT"])
    book_routes.add_url_rule("/books/<int:id>", view_func=book_service.delete, methods=["DELETE"])

    return book_routes
