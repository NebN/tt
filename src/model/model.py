import os


class Text:
    def __init__(self, text=None, lines=None):
        assert(text is not None or lines is not None)
        self._text = text
        self._lines = lines

    def text(self):
        if self._text is None:
            self._text = os.linesep.join(self._lines)
        return self._text

    def lines(self):
        if self._lines is None:
            self._lines = self._text.splitlines()
        return self._lines

    def __repr__(self):
        return self.text()
