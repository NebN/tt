from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QFont


class Dialog(QDialog):
    def __init__(self, master=None, title='', message=''):
        QDialog.__init__(self, master)
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle(title)
        font = QFont()
        font.setPointSize(10)
        margins = QMargins(10, 5, 10, 5)
        label = QLabel(message)
        label.setFont(font)
        label.setContentsMargins(margins)
        layout = QVBoxLayout(self)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.show()