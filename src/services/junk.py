from services.database import DatabaseService
from sqlite3 import IntegrityError

_JunkService_instance = None

class JunkService:

    def __init__(self):
        pass

    def count(self):
        db = DatabaseService.get_instance()
        sql = "SELECT COUNT(*) FROM junk"
        rows = db.execute_select(sql, ())
        return rows[0][0]

    def append(self, word_token):
        db = DatabaseService.get_instance()
        try:
            sql = "INSERT INTO junk (token) VALUES (?)"
            db.execute_insert(sql, (word_token.token,))
            return True
        except IntegrityError as e:
            if "UNIQUE constraint failed: junk.token" in str(e):
                return False

    def is_junk(self, word_token):
        db = DatabaseService.get_instance()
        sql = "SELECT token FROM junk where TOKEN=?"
        rows = db.execute_select(sql, (word_token.token,))
        return len(rows) == 1

    @staticmethod
    def sql_create_table(db_cursor):
        db_cursor.execute('''
            CREATE TABLE junk (
                token str unique
            )
        ''')

    @staticmethod
    def get_instance():
        global _JunkService_instance
        if _JunkService_instance is None:
            _JunkService_instance = JunkService()
        return _JunkService_instance