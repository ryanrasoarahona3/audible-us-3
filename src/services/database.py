import sqlite3

_DatabaseService_instance = None

class DatabaseService:
    _db_path: str
    _con: str

    def set_db_path(self, db_path):
        self._db_path = db_path
        self._con = sqlite3.connect(self._db_path)

    def get_cursor(self):
        return self._con.cursor()

    def execute_query(self, sql, object=None):
        self._con.execute(sql, object)
        self._con.commit()

    def execute_insert(self, sql, object, return_row_id=False):
        cursor = self._con.cursor()
        cursor.execute(sql, object)
        self._con.commit()
        return cursor.lastrowid

    def execute_select(self, sql, params):
        cursor = self._con.cursor()
        cursor.execute(sql, params)
        return cursor.fetchall()

    @staticmethod
    def get_instance():
        global _DatabaseService_instance
        if _DatabaseService_instance is None:
            _DatabaseService_instance = DatabaseService()
        return _DatabaseService_instance
