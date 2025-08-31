from flask import Flask, jsonify
from flask_mysqldb import MySQL 
from config.db import Config
from routes.bookRoutes import book_routes, init_routes

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)
init_routes(mysql)

app.register_blueprint(book_routes)

@app.route("/")
def home():
    return jsonify({"message": "API Flask + MySQL rodando!"})

if __name__ == "__main__":
    app.run(debug=True)