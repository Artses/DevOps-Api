from flask import jsonify, request
from models.book import Book

class BookController:
    def __init__(self, mysql):
        self.mysql = mysql
    
    def get_all(self):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM books")
        rows = cur.fetchall()
        cur.close()
        books = [Book(id=row[0], title=row[1], author=row[2]).to_dict() for row in rows]
        return jsonify(books)
    
    def get_by_id(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s", (id,))
        row = cur.fetchone()
        cur.close()
        if not row:
            return jsonify({"error": "Livro não encontrado"}), 404
        return jsonify(Book(id=row[0], title=row[1], author=row[2]).to_dict())
    
    def create(self):
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        if not title or not author:
            return jsonify({"error": "Campos faltando"}), 400
        cur = self.mysql.connection.cursor()
        cur.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        self.mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Livro adicionado com sucesso"}), 201

    def update(self, id):
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        if not title or not author:
            return jsonify({"error": "Campos faltando"}), 400
        
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s", (id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            return jsonify({"error": "Livro não encontrado"}), 404
        
        cur.execute("UPDATE books SET title=%s, author=%s WHERE id=%s", (title, author, id))
        self.mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Livro atualizado com sucesso!"})
        
    def delete(self, id):
        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM books WHERE id=%s", (id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            return jsonify({"error": "Livro não encontrado"}), 404
        cur.execute("DELETE FROM books WHERE id=%s", (id,))
        self.mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Livro deletado com sucesso!"})
