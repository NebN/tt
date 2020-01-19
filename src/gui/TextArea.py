from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import pyqtSignal


class TextArea(QPlainTextEdit):

    keyPressed = pyqtSignal('QKeyEvent')

    def __init__(self, master):
        QPlainTextEdit.__init__(self, master)
        self.setLineWrapMode(False)

    # Override
    def keyPressEvent(self, event):
        QPlainTextEdit.keyPressEvent(self, event)
        self.keyPressed.emit(event)

    def get(self):
        return self.toPlainText()

    def set(self, text):
        self.setPlainText(text)
