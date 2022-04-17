from dataclasses import dataclass
from services.database import DatabaseService
from services.junk import JunkService
from sqlite3 import IntegrityError
from nltk.stem.snowball import EnglishStemmer
from nltk import RegexpTokenizer
_stemmer = EnglishStemmer()
_tokenizer = RegexpTokenizer("[a-zA-Z]+")

@dataclass
class WordToken:
    id: int       # primary, not mutable
    token: str    # unique, not mutable
    stem: str
    definitions: str

    def __init__(self, token, stem=None, id=None, definitions=None):
        self.token = token.lower()
        if stem is not None:
            self.stem = stem
        else:
            self.stem = _stemmer.stem(token)
        self.id = id
        self.definitions = definitions

    def persist(self):
        db = DatabaseService.get_instance()
        if self.id is None:
            try:
                sql = "INSERT INTO word_token (token, stem, definitions) VALUES (?, ?, ?)"
                self.id = db.execute_insert(sql, (self.token, self.stem, self.definitions))
                return True
            except IntegrityError as e:
                if "UNIQUE constraint failed: word_token.token" in str(e):
                    duplicate = WordToken.from_db_fetch_from_token(self.token)
                    self.id = duplicate.id
                    self.stem = duplicate.stem
                    self.definitions = duplicate.definitions
                    return False
        else:
            sql = "UPDATE word_token SET stem=?, definitions=? WHERE id=?"
            db.execute_query(sql, (self.stem, self.definitions, str(self.id)))

    def is_junk(self):
        js = JunkService.get_instance()
        return js.is_junk(self)

    def junk(self):
        js = JunkService.get_instance()
        return js.append(self)

    @staticmethod
    def sql_create_table(db_cursor):
        db_cursor.execute('''
            CREATE TABLE word_token (
                id integer primary key autoincrement,
                token str unique,
                stem str,
                definitions str
            )
        ''')

    @staticmethod
    def _from_sqlite_plain_tuple(tuple):
        return WordToken(
            id=tuple[0],
            token=tuple[1],
            stem=tuple[2],
            definitions=tuple[3]
        )

    @staticmethod
    def from_db_fetch_all():
        # Contrary to the other data class
        # Book Content should be loaded manually
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, token, stem, definitions FROM word_token", ())
        rows = [WordToken._from_sqlite_plain_tuple(row) for row in rows]
        return rows

    @staticmethod
    def from_db_fetch_from_id(token_id):
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, token, stem, definitions FROM word_token WHERE id = ?", (str(token_id),))
        if len(rows) == 0:
            raise Exception("Token not found")
        else:
            row = rows[0]
            return WordToken._from_sqlite_plain_tuple(row)

    @staticmethod
    def from_db_fetch_from_token(token):
        db = DatabaseService.get_instance()
        rows = db.execute_select("SELECT id, token, stem, definitions FROM word_token WHERE token = ?", (token, ))
        if len(rows) == 0:
            raise Exception("Token not found")
        else:
            row = rows[0]
            return WordToken._from_sqlite_plain_tuple(row)

    @staticmethod
    def tokenize(text):
        text = text.lower()
        words = _tokenizer.tokenize(text)
        output = [WordToken(word) for word in words]
        return output
