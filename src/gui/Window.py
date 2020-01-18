from tkinter import *
from .TextWindow import TextWindow


class Window(Frame):

    def __init__(self, master):
        Frame.__init__(self, master=None)
        verticalpane = PanedWindow(self, orient=VERTICAL)

        topsection = Frame(self)

        self.infostring = StringVar()
        self.infostring.set('.* welcome .*')
        infolabel = Label(topsection, height=1, textvariable=self.infostring, relief=FLAT)
        infolabel.pack(fill=X, expand=0)
        self.codeinput = TextWindow(topsection, height=3)
        self.codeinput.pack(fill=BOTH, expand=1)

        horizontalpane = PanedWindow(verticalpane, orient=HORIZONTAL)
        self.left = TextWindow(horizontalpane)
        self.right = TextWindow(horizontalpane, readonly=True)
        horizontalpane.add(self.left)
        horizontalpane.add(self.right)
        horizontalpane.pack(fill=BOTH, expand=1)

        verticalpane.add(topsection)
        verticalpane.add(horizontalpane)
        verticalpane.pack(fill=BOTH, expand=1)

    def code(self):
        return self.codeinput.text()

    def inputtext(self):
        return self.left.text()

    def setoutput(self, output):
        self.right.settext(output)
