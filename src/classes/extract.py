from dataclasses import dataclass
from classes.book import Book
from services.database import DatabaseService
from classes.word_token import WordToken
from classes.word_occurrence import WordOccurrence

from nltk.stem.snowball import EnglishStemmer
from nltk import RegexpTokenizer
_stemmer = EnglishStemmer()
_tokenizer = RegexpTokenizer("[a-zA-Z]+")

@dataclass
class Extract:
    id: int
    book_id: int
    line_from: int
    line_to: int

    def __init__(self, book_id, line_from, line_to, id=None):
        self.book_id = book_id
        self.line_from = line_from
        self.line_to = line_to
        self.id = id
        self._book = None
        self._content = None
        self._word_occurrences = None

    def get_book(self):
        if self._book is None:
            self._book = Book.from_db_fetch_from_id(self.book_id)
        return self._book
    book = property(get_book, None, None)

    def get_content(self):
        if self._content is None:
            book_content = self.book.content
            book_lines = book_content.split("\n")
            extract_lines = book_lines[self.line_from:self.line_to+1]
            return "\n".join(extract_lines)
        return self._content
    content = property(get_content, None, None)

    def persist(self):
        db = DatabaseService.get_instance()
        if self.id is None:
            sql = "INSERT INTO extract (book_id, line_from, line_to) VALUES (?, ?, ?)"
            self.id = db.execute_insert(sql, (self.book_id, self.line_from, self.line_to))

    # experimental feature
    # junks will not be considered as word
    # normally, junks won't be inserted into database
    def get_word_occurrences(self):
        if self._word_occurrences is None:
            output = []
            lines = self.content.split("\n")
            for i, line in enumerate(lines):
                words = _tokenizer.tokenize(line)
                for word in words:
                    word_token = WordToken(word)
                    if not word_token.is_junk():
                        word_token.persist()
                        output.append(WordOccurrence(
                            token_id=word_token.id,
                            book_id=self.book_id,
                            line_id=self.line_from + i
                        ))
            self._word_occurrences = output
        return self._word_occurrences
    word_occurrences = property(get_word_occurrences, None, None)

    @staticmethod
    def sql_create_table(db_cursor):
        db_cursor.execute('''
            CREATE TABLE extract (
                id integer primary key autoincrement,
                book_id integer,
                line_from integer,
                line_to integer,
                foreign key (book_id) references book(id) on delete cascade
            )
        ''')