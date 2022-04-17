import unittest
import os
from classes.book import Book
from classes.extract import Extract
from classes.word_token import WordToken
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
        WordToken.sql_create_table(self.db.get_cursor())

        # Creating book class
        self.example_book = Book("the-title.txt", BOOK_CONTENT)
        self.example_book.persist()

    def test_token_insertion(self):
        self.init_db()

        tok1 = WordToken("spaceplane")
        tok2 = WordToken("warship")
        self.assertIsNone(tok1.id)
        self.assertIsNone(tok2.id)

        tok1.persist()
        tok2.persist()
        self.assertIsNotNone(tok1.id)
        self.assertIsNotNone(tok2.id)

    def test_unique_field(self):
        self.init_db()

        w1 = WordToken("the")
        w2 = WordToken("pilot")
        w3 = WordToken("the")
        w1.persist()
        w2.persist()
        w3.persist()

        self.assertEqual(w3.id, w1.id)
        self.assertEqual(w3.stem, w3.stem)
        self.assertEqual(w3.definitions, w3.definitions)

    def test_tokenize(self):
        self.init_db()

        sentence = "The pilot saw the coastline"
        words = WordToken.tokenize(sentence)
        [word.persist() for word in words]

        token_list = WordToken.from_db_fetch_all()
        self.assertEqual(len(token_list), 4)

    def test_token_definition_principle(self):
        self.init_db()

        text1 = "The windshield breaks down."
        words1 = WordToken.tokenize(text1)
        [word.persist() for word in words1]

        word_windshield = WordToken.from_db_fetch_from_token("windshield")
        self.assertEqual(word_windshield.id, 2)
        word_windshield.definitions = "parebrise"
        word_windshield.persist()

        text2 = "He won't buy a new windshield."
        words2 = WordToken.tokenize(text2)
        [word.persist() for word in words2]

        word_windshield_2 = words2[6]
        self.assertEqual(word_windshield_2.id, 2)
        self.assertEqual(word_windshield_2.definitions, "parebrise")
        word_windshield_2.definitions = "parebrise, pare-vent"
        word_windshield_2.persist()

        word_windshield_3 = WordToken.from_db_fetch_from_token("windshield")
        self.assertEqual(word_windshield_3.definitions, "parebrise, pare-vent")


if __name__ == '__main__':
    unittest.main()
