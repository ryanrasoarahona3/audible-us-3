from dataclasses import dataclass
from classes.book import Book
from classes.word_token import WordToken
from services.database import DatabaseService
from services.junk import JunkService

@dataclass
class WordOccurrence:
    id: int
    token_id: int
    book_id: int
    line_id: int  # Not a foreign key

    def __init__(self, token_id, book_id, line_id, id=None):
        self.token_id = token_id
        self.book_id = book_id
        self.line_id = line_id
        self.id = id
        self._token = None
        self._book = None

    def get_book(self):
        if self._book is None:
            self._book = Book.from_db_fetch_from_id(self.book_id)
        return self._book
    book = property(get_book, None, None)

    def get_token(self):
        if self._token is None:
            self._token = WordToken.from_db_fetch_from_id(self.token_id)
        return self._token
    token = property(get_token)

    def persist(self):
        db = DatabaseService.get_instance()
        if self.id is None:
            sql = "INSERT INTO word_occurrence (token_id, book_id, line_id) VALUES (?, ?, ?)"
            self.id = db.execute_insert(sql, (self.token_id, self.book_id, self.line_id))

    def is_junk(self):
        js = JunkService.get_instance()
        return js.is_junk(self.token)

    def junk(self):
        js = JunkService.get_instance()
        return js.append(self.token)

    @staticmethod
    def _from_sqlite_plain_tuple(tuple):
        return WordToken(
            id=tuple[0],
            token_id=tuple[1],
            book_id=tuple[2],
            line_id=tuple[3]
        )

    @staticmethod
    def from_db_fetch_all():
        # Contrary to the other data class
        # Book Content should be loaded manually
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, token_id, book_id, line_id FROM word_occurrence", ())
        rows = [WordOccurrence._from_sqlite_plain_tuple(row) for row in rows]
        return rows

    @staticmethod
    def from_db_fetch_from_id(occurrence_id):
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, token_id, book_id, line_id  FROM word_occurrence WHERE id = ?", (str(occurrence_id)))
        if len(rows) == 0:
            raise Exception("Occurrence not found")
        else:
            row = rows[0]
            return WordOccurrence._from_sqlite_plain_tuple(row)

    @staticmethod
    def sql_create_table(db_cursor):
        db_cursor.execute('''
            CREATE TABLE word_occurrence (
                id integer primary key autoincrement,
                token_id integer,
                book_id integer,
                line_id integer,
                foreign key (token_id) references  word_token(id) on delete cascade,
                foreign key (book_id) references book(id) on delete cascade
            )
        ''')