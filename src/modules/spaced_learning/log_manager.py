
class LogManager:
    def __init__(self, file_path):
        self._log_data = []
        self.file_path = file_path
        self._load_logs()
        self._additionnal = []

    def _load_logs(self):
        with open(self.file_path, 'r', encoding='utf8') as f:
            lines = f.read().split('\n')
            self._log_data = [l.split('\t') for l in lines]
            self._log_data = [[int(l[0]), l[1], int(l[2]), float(l[3])] for l in self._log_data
                              if len(l) == 4]

    def append(self, card):
        self._additionnal.append(f'{card.last}\t{card.name}\t{card.ivl}\t{card.ease}')

    def flush(self):
        with open(self.file_path, 'a', encoding='utf8') as f:
            f.write('\n')
            f.write('\n'.join(self._additionnal))
        self._additionnal = []
