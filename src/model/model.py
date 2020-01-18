import os


class Text:
    def __init__(self, text=None, lines=None):
        self._text = text
        self._lines = lines

    def text(self):
        if not self._text:
            self._text = os.linesep.join(self._lines)
        return self._text

    def lines(self):
        if not self._lines:
            self._lines = self._text.splitlines()
        return self._lines

    def __repr__(self):
        return self.text()