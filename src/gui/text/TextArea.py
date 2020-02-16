from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtProperty, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QTextCursor
from src.gui import Color
from src.util import StyleUtils


class TextArea(QPlainTextEdit):
    keyPressed = pyqtSignal('QKeyEvent')

    def __init__(self, master, pointsize=8):
        QPlainTextEdit.__init__(self, master)
        self.default_format = self.currentCharFormat()
        self.cursor = self.textCursor()
        font = QFont()
        font.setPointSize(pointsize)
        self.setFont(font)
        self.setLineWrapMode(False)
        self.animation = QPropertyAnimation(self, b'bordercolor')
        self.setStyleSheet(self.styleSheet() + 'border: 1px solid;')

    # Override
    def keyPressEvent(self, event):
        QPlainTextEdit.keyPressEvent(self, event)
        self.cursor.select(QTextCursor.Document)
        self.cursor.setCharFormat(self.default_format)
        self.keyPressed.emit(event)

    def get(self):
        return self.toPlainText()

    def set(self, text):
        self.setPlainText(text)

    def setbordercolor(self, color):
        updated_style = StyleUtils.change_property(self.styleSheet(), 'border-color', StyleUtils.color_as_css(color))
        self.setStyleSheet(updated_style)

    def getbordercolor(self):
        style = StyleUtils.get_property(self.styleSheet(), 'border-color')
        if style:
            return StyleUtils.css_as_color(style)
        else:
            return Color.BLACK

    @pyqtProperty(QColor)
    def bordercolor(self):
        return self.getbordercolor()

    @bordercolor.setter
    def bordercolor(self, color):
        self.setbordercolor(color)

    def flash(self, color, end=None):
        endvalue = end if end else self.bordercolor
        self.animation.stop()
        self.animation.setStartValue(color)
        self.animation.setEndValue(endvalue)
        self.animation.setDuration(700)
        self.animation.setEasingCurve(QEasingCurve.InExpo)
        self.animation.start()


palette_window = QPalette.Window
bordercolor = pyqtProperty(QColor)
