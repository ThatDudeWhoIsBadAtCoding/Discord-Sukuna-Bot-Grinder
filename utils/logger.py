from io import StringIO
import pyperclip

class Logger():
    def __init__(self, pulls=9):
        self.pulls = pulls
        self.logging = True
        self._sacrifices = []

    @property
    def sacrifices(self):
        no_dupes = set(self._sacrifices)
        sacrifice_string = StringIO()
        for card in no_dupes:
            sacrifice_string.write(f"{card}: {self._sacrifices.count(card)}, ")
        pyperclip.copy(sacrifice_string.getvalue()[:-2])
        return sacrifice_string.getvalue()[:-2]
    
    @sacrifices.setter
    def sacrifices(self, value):
        self._sacrifices = value
        return

    def log(self, card_name, amount):
        with open("ace_tracker.txt", "r") as file:
            for line in file.readlines():
                if not line.startswith("-"):
                    current_parent = line.split("-")[1]
                if card_name in line:
                    return current_parent
        if card_name in self.sacrifices:
            self._sacrifices.append(card_name)
        else:
            self._sacrifices.extend([card_name for _ in range(int(amount))])
        return None

