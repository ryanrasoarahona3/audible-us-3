import unittest

import sys
sys.path.append("../src/modules/spaced_learning")
from modules.spaced_learning.card import Card

class MyTestCase(unittest.TestCase):
    def test_modules(self):
        obj = Card(
            name="name",
            last=0,
            ivl=60,
            ease=3
        )
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
