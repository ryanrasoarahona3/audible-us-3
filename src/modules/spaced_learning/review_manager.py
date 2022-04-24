import random

from log_manager import LogManager
from card import Card
import time
import random

class ReviewManager(LogManager):
    def __init__(self, file_path, time_provider=time):
        self.file_path = file_path
        self.time_provider = time_provider
        super().__init__(file_path)
        self._load_deck()
        self._review_list = None

    def _load_deck(self):
        d = self._log_data
        added_card = []
        self._deck = []
        for card_data in self._log_data:
            [last, name, ivl, ease] = card_data
            if name not in added_card:
                added_card.append(name)
                self._deck.append(
                    Card(last, name, ivl, ease)
                )
            else:
                self._deck[added_card.index(name)].patch(
                    last, ivl, ease
                )

    def card_by_name(self, name):
        output = [c for c in self._deck if c.name == name]
        return None if len(output) == 0 else output[0]

    def reschedule(self, name, rating):
        card = self.card_by_name(name)
        # ipl should be defined
        ipl = (self.time_provider.time() - card.last) / card.ivl
        # ipl = 2.1 if ipl > 2.5 else ipl
        ipl = 2.5 if ipl > 2.5 else ipl

        if rating == -1:  # HARD
            card.ivl = 60
            card.ease = card.ease - ipl * 0.15
        if rating == 1:  # EASY
            card.ivl = card.ivl + card.ivl * (card.ease - 1) * ipl  # 1-不知道　
            card.ease = card.ease + ipl * 0.2

        card.ease = 1.2 if card.ease < 1.2 else card.ease
        card.ivl = int(card.ivl)
        card.last = int(self.time_provider.time())

        # Log manager prototype
        self.append(card)

    def new_card(self, name):
        new_card = Card.create(name)
        self._deck.append(new_card)
        self.append(new_card)

    def next_review(self):
        # Next review
        possibles = []
        for c in self._deck:
            if self._review_list is not None:
                if c.name not in self._review_list :
                    continue
            if c.last + c.ivl < self.time_provider.time():  # late
                possibles.append(c.name)
        if len(possibles) == 0:
            return None
        return possibles[random.randint(0, len(possibles)-1)]

    def card_list(self):
        o = [c.name for c in self._deck]
        if self._review_list is not None:
            return [c for c in o if c in self._review_list]
        return o

    def late_list(self):
        o = [c.name for c in self._deck if c.last + c.ivl < self.time_provider.time()]
        if self._review_list is not None:
            return [c for c in o if c in self._review_list]
        return o

    def add_review_list(self, list):
        self._review_list = list