import unittest
import os
from classes.book import Book
from classes.extract import Extract
from services.database import DatabaseService


BOOK_CONTENT = """
Thanks to all who gave their lives on the high frontier.

FLIGHT Test

The pilot saw the coastline as a smudge stretching across the horizon. Beyond the cockpit's windshield she could see that the sky was bright.

The spaceplane arrowed across the sky and crossed the California at an altitude of 197,000 feet. The plane's nose was bright with a new morning coming up.

"""

class MyTestCase(unittest.TestCase):
    def init_db(self):
        self.db = DatabaseService.get_instance()
        if os.path.exists("../data/db_test.sqlite"):
            os.remove("../data/db_test.sqlite")
        self.db.set_db_path("../data/db_test.sqlite")

        # Creating tables
        Book.sql_create_table(self.db.get_cursor())
        Extract.sql_create_table(self.db.get_cursor())

        # Creating book class
        self.example_book = Book("the-title.txt", BOOK_CONTENT)
        self.example_book.persist()

    def test_adding_extract(self):
        self.init_db()
        extract = Extract(
            book_id=self.example_book.id,
            line_from=0,
            line_to=2
        )

        extract.persist()
        self.assertEqual(extract.id, 1)

    def test_extract_book_detail(self):
        self.init_db()
        extract = Extract(
            book_id=self.example_book.id,
            line_from=5,
            line_to=7
        )
        book = extract.book
        self.assertEqual(book.file, "the-title.txt")

    def test_extract_content(self):
        self.init_db()
        extract = Extract(
            book_id=self.example_book.id,
            line_from=5,
            line_to=7
        )
        content = extract.content
        self.assertNotIn("FLIGHT", content)
        self.assertIn("The pilot", content)
        self.assertIn("The spaceplane", content)


if __name__ == '__main__':
    unittest.main()
