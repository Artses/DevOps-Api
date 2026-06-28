# Books API

Flask API backed by MySQL.

## Setup

Start MySQL:

```bash
docker run --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=your_secure_password \
  -p 3306:3306 \
  -v mysql_data:/var/lib/mysql \
  -d mysql:latest
```

Create `.env` from `.env.example`, then install dependencies:

```bash
cp .env.example .env
.venv/bin/pip install -r requirements.txt
```

Run the API:

```bash
.venv/bin/python app.py
```

The app creates the `testdb` database and `books` table automatically if they do not exist.

## Endpoints

- `GET /books`
- `GET /books/<id>`
- `POST /books`
- `PUT /books/<id>`
- `DELETE /books/<id>`

Example request:

```bash
curl -X POST http://localhost:5000/books \
  -H "Content-Type: application/json" \
  -d '{"title":"Clean Code","author":"Robert C. Martin"}'
```
