from tkinter import Text, END
from src.model import Text as TextLines


class TextWindow(Text):

    def __init__(self, master, readonly=False, **kw):
        super().__init__(master, **kw)
        if readonly:
            self.bind('<Key>', lambda e: 'break')

    def settext(self, text):
        self.delete(1.0, END)
        self.insert(index=END, chars=text)

    def addtext(self, text):
        self.insert(index=END, chars=text)

    def text(self):
        return self.get(index1="1.0", index2=END)

