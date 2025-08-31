from flask import Blueprint
from controller.bookController import BookController

book_routes = Blueprint('bookRoutes', __name__)
book_controller = None

def init_routes(mysql):
    global book_controller
    book_controller = BookController(mysql)

    book_routes.add_url_rule("/books", view_func=book_controller.get_all, methods=['GET'])
    book_routes.add_url_rule("/books/<int:id>", view_func=book_controller.get_by_id, methods=['GET'])
    book_routes.add_url_rule("/books", view_func=book_controller.create, methods=['POST'])
    book_routes.add_url_rule("/books/<int:id>", view_func=book_controller.update, methods=['PUT'])
    book_routes.add_url_rule("/books/<int:id>", view_func=book_controller.delete, methods=['DELETE'])

    

