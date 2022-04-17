from dataclasses import dataclass
from services.database import DatabaseService

@dataclass
class Book:
    id: int
    file: str
    content: str

    def __init__(self, file, content, id=None):
        self.id = id # is only set by the database service
        self.file = file
        self.content = content

    def persist(self):
        db = DatabaseService.get_instance()
        if self.id is None: # insert
            sql = "INSERT INTO book (file, content) VALUES (?, ?)"
            self.id = db.execute_insert(sql, (self.file, self.content))
        else :
            sql = "UPDATE book SET file=?, content=? WHERE id=?"
            db.execute_query(sql, (self.file, self.content, str(self.id)))

    def delete(self):
        db = DatabaseService.get_instance()
        if self.id is not None:
            sql = "DELETE FROM book WHERE id=?"
            db.execute_query(sql, (str(self.id)))
            self.id = None

    @staticmethod
    def sql_create_table(db_cursor):
        db_cursor.execute('''
            CREATE TABLE book (
                id integer primary key autoincrement,
                file text,
                content text
            )
        ''')

    @staticmethod
    def _from_sqlite_plain_tuple(tuple):
        return Book(
            id=tuple[0],
            file=tuple[1],
            content=""
        )

    @staticmethod
    def from_db_fetch_all():
        # Contrary to the other data class
        # Book Content should be loaded manually
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, file FROM book", ())
        rows = [Book._from_sqlite_plain_tuple(row) for row in rows]
        return rows

    @staticmethod
    def from_db_fetch_from_id(book_id):
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, file, content FROM book WHERE id = ?", (str(book_id)))
        if len(rows) == 0 :
            raise Exception("Book not found")
        else :
            row = rows[0]
            return Book(
                id=row[0],
                file=row[1],
                content=row[2]
            )