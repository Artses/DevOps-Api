import pymysql
from flask import current_app, g

class MySQL:
    def init_app(self, app):
        self.create_schema(app)
        app.teardown_appcontext(self.close)

    @property
    def connection(self):
        if "mysql_connection" not in g:
            g.mysql_connection = pymysql.connect(
                host=current_app.config["MYSQL_HOST"],
                user=current_app.config["MYSQL_USER"],
                password=current_app.config["MYSQL_PASSWORD"],
                database=current_app.config["MYSQL_DB"],
                charset="utf8mb4",
            )

        return g.mysql_connection

    def create_schema(self, app):
        database = app.config["MYSQL_DB"]
        self._validate_database_name(database)

        connection = pymysql.connect(
            host=app.config["MYSQL_HOST"],
            user=app.config["MYSQL_USER"],
            password=app.config["MYSQL_PASSWORD"],
            charset="utf8mb4",
            autocommit=True,
        )

        try:
            with connection.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database}`")
                cursor.execute(f"USE `{database}`")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS books (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                    """
                )
        finally:
            connection.close()

    def close(self, error=None):
        connection = g.pop("mysql_connection", None)
        if connection is not None:
            connection.close()

    def _validate_database_name(self, database):
        if not database or not database.replace("_", "").isalnum():
            raise ValueError("MYSQL_DB must contain only letters, numbers, and underscores")
