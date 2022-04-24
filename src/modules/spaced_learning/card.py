import time

class Card:
    def __init__(self, last, name, ivl, ease):
        self.last = last
        self.name = name
        self.ivl = ivl
        self.ease = ease

    def patch(self, last, ivl, ease):
        self.last = last
        self.ivl = ivl
        self.ease = ease

    @staticmethod
    def create(name):
        return Card(int(time.time()), name, 60, 2.1)