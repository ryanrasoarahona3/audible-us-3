import unittest
import os

from classes.book import Book
from classes.extract import Extract
from classes.word_token import WordToken
from classes.word_occurrence import WordOccurrence
from services.database import DatabaseService
from services.junk import JunkService

BOOK_CONTENT = """
FLIGHT TEST OF MATAGORDA

The windshield breaks down after he saw the coastline.

The swarm of reporters waits for him to get off the plane.

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
        WordToken.sql_create_table(self.db.get_cursor())
        WordOccurrence.sql_create_table(self.db.get_cursor())
        JunkService.sql_create_table(self.db.get_cursor())

        # Creating book class
        self.example_book = Book("the-title.txt", BOOK_CONTENT)
        self.example_book.persist()

    def test_word_occurrrences(self):
        self.init_db()

        extract1 = Extract(
            book_id=self.example_book.id,
            line_from=1,
            line_to=3
        )
        extract1.persist()
        occurrences = extract1.word_occurrences
        self.assertEqual(13, len(occurrences), "13 should be in occurrences for extract 1")
        # windshield, coastline are the difficult words
        # Mark all occurrences as junk, except for those two difficult words
        hard_occurences = []
        for occurence in occurrences:
            if occurence.token.token not in ["windshield", "coastline"] :
                occurence.junk()
            else: # Hard occurrence
                hard_occurences.append(occurence)

        extract2 = Extract(
            book_id=self.example_book.id,
            line_from=5,
            line_to=5
        )
        extract2.persist()
        occurrences = extract2.word_occurrences
        self.assertEqual(9, len(occurrences), "9 should be in occurrences for extract 2")

        # swarm is the difficult word
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()
