import unittest
import os
from classes import book
from services.database import DatabaseService
from classes.book import Book


class MyTestCase(unittest.TestCase):

    def init_db(self):
        self.db = DatabaseService.get_instance()
        if os.path.exists("../data/db_test.sqlite"):
            os.remove("../data/db_test.sqlite")
        self.db.set_db_path("../data/db_test.sqlite")

        # Creating tables
        Book.sql_create_table(self.db.get_cursor())

    def test_book_insertion(self):
        self.init_db()

        book1 = Book(file="file.txt", content="book content")
        self.assertIsNone(book1.id)

        book1.persist()
        self.assertIsNotNone(book1.id)

    def test_book_listing(self):
        self.init_db()

        book1 = Book(file="book1.txt", content="This is the book 1")
        book2 = Book(file="book2.txt", content="This is the book 2")
        book3 = Book(file="book3.txt", content="This is the book 3")
        book1.persist()
        book2.persist()
        book3.persist()

        book_list = Book.from_db_fetch_all()
        self.assertEqual(len(book_list), 3, "Book count should be 3")

        book_files = [b.file for b in book_list]
        self.assertIn("book2.txt", book_files, "Contains book2.txt")
        self.assertIn("book3.txt", book_files, "Contains book3.txt")

    def test_book_search(self):
        self.init_db()

        book1 = Book(file="book1.txt", content="This is the book 1")
        book2 = Book(file="book2.txt", content="This is the book 2")
        book3 = Book(file="book3.txt", content="This is the book 3")
        book1.persist()
        book2.persist()
        book3.persist()

        # Search for book3
        book_id = book3.id
        book_r = Book.from_db_fetch_from_id(book_id)
        self.assertEqual(book_r.file, "book3.txt")


    def test_book_update(self):
        self.init_db()

        book1 = Book(file="book1.txt", content="This is the book 1")
        book2 = Book(file="book2.txt", content="This is the book 2")
        book3 = Book(file="book3.txt", content="This is the book 3")
        book1.persist()
        book2.persist()
        book3.persist()

        # Search for book3
        book_id = book3.id
        book_r = Book.from_db_fetch_from_id(book_id)
        book_r.file = "the-book.txt"
        book_r.persist()

    def test_delete(self):
        self.init_db()

        book1 = Book(file="book1.txt", content="This is the book 1")
        book2 = Book(file="book2.txt", content="This is the book 2")
        book3 = Book(file="book3.txt", content="This is the book 3")
        book1.persist()
        book2.persist()
        book3.persist()

        book2.delete()
        book_list = Book.from_db_fetch_all()
        self.assertEqual(len(book_list), 2)


if __name__ == '__main__':
    unittest.main()
