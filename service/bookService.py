from flask import jsonify, request

class BookService:
    def __init__(self, mysql):
        self.mysql = mysql

    def _error(self, message, status_code):
        return jsonify({"error": message}), status_code

    def _read_payload(self):
        data = request.get_json(silent=True)
        if data is None:
            return None, self._error("Request body must be valid JSON", 400)

        title = data.get("title")
        author = data.get("author")

        if not isinstance(title, str) or not title.strip():
            return None, self._error("Field 'title' is required", 400)

        if not isinstance(author, str) or not author.strip():
            return None, self._error("Field 'author' is required", 400)

        return {"title": title.strip(), "author": author.strip()}, None

    def _book_from_row(self, row):
        return {"id": row[0], "title": row[1], "author": row[2]}
    
    def get_all(self):
        cur = None
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT id, title, author FROM books ORDER BY id")
            rows = cur.fetchall()
        finally:
            if cur:
                cur.close()

        books = [self._book_from_row(row) for row in rows]
        return jsonify(books)
    
    def get_by_id(self, id):
        cur = None
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT id, title, author FROM books WHERE id=%s", (id,))
            row = cur.fetchone()
        finally:
            if cur:
                cur.close()

        if not row:
            return self._error("Book not found", 404)

        return jsonify(self._book_from_row(row))
    
    def create(self):
        data, error = self._read_payload()
        if error:
            return error

        cur = None
        try:
            cur = self.mysql.connection.cursor()
            cur.execute(
                "INSERT INTO books (title, author) VALUES (%s, %s)",
                (data["title"], data["author"]),
            )
            self.mysql.connection.commit()
            book_id = cur.lastrowid
        except Exception:
            self.mysql.connection.rollback()
            raise
        finally:
            if cur:
                cur.close()

        return jsonify({"id": book_id, **data}), 201

    def update(self, id):
        data, error = self._read_payload()
        if error:
            return error

        cur = None
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("SELECT id FROM books WHERE id=%s", (id,))
            if not cur.fetchone():
                return self._error("Book not found", 404)

            cur.execute(
                "UPDATE books SET title=%s, author=%s WHERE id=%s",
                (data["title"], data["author"], id),
            )
            self.mysql.connection.commit()
        except Exception:
            self.mysql.connection.rollback()
            raise
        finally:
            if cur:
                cur.close()

        return jsonify({"id": id, **data})
        
    def delete(self, id):
        cur = None
        try:
            cur = self.mysql.connection.cursor()
            cur.execute("DELETE FROM books WHERE id=%s", (id,))

            if cur.rowcount == 0:
                self.mysql.connection.rollback()
                return self._error("Book not found", 404)

            self.mysql.connection.commit()
        except Exception:
            self.mysql.connection.rollback()
            raise
        finally:
            if cur:
                cur.close()

        return "", 204
