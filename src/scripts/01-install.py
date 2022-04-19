
import os
from glob import glob

from classes.book import Book
from classes.extract import Extract
from classes.word_token import WordToken
from classes.word_occurrence import WordOccurrence
from services.database import DatabaseService
from services.junk import JunkService


db = DatabaseService.get_instance()

def init_db():
    global db
    if os.path.exists("../../data/db_prod.sqlite"):
        os.remove("../../data/db_prod.sqlite")
    db.set_db_path("../../data/db_prod.sqlite")

    # Creating tables
    Book.sql_create_table(db.get_cursor())
    Extract.sql_create_table(db.get_cursor())
    WordToken.sql_create_table(db.get_cursor())
    WordOccurrence.sql_create_table(db.get_cursor())
    JunkService.sql_create_table(db.get_cursor())

def seeding_book():
    book_list = glob("../../data/books/*.txt")
    for book in book_list:
        with open(book, "r", encoding="utf8") as f:
            book_content = f.read()
        book_file = book[book.rindex("/")+1:]
        book_object = Book(file=book_file, content=book_content)
        book_object.persist()


if __name__ == '__main__':
    init_db()
    seeding_book()