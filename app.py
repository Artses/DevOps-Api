from flask import Flask, jsonify
from config.db import Config
from config.mysql import MySQL
from routes.bookRoutes import create_book_blueprint

mysql = MySQL()

def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    mysql.init_app(app)
    app.register_blueprint(create_book_blueprint(mysql))

    @app.route("/")
    def home():
        return jsonify({"status": "ok", "message": "Books API is running"})

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
