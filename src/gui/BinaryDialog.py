from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QFont


class BinaryDialog(QDialog):
    def __init__(self, master=None, title='', message=''):
        QDialog.__init__(self, master)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowTitle(title)
        font = QFont()
        font.setPointSize(10)
        margins = QMargins(10, 5, 10, 5)
        label = QLabel(message)
        label.setFont(font)
        label.setContentsMargins(margins)

        button_layout = QHBoxLayout(self)

        self.yes = QPushButton('Yes')
        self.yes.clicked.connect(lambda: self.close())
        self.no = QPushButton('No')
        self.no.clicked.connect(lambda: self.close())
        self.cancel = QPushButton('Cancel')
        self.cancel.clicked.connect(lambda: self.close())
        button_layout.addWidget(self.yes)
        button_layout.addWidget(self.no)
        button_layout.addWidget(self.cancel)
        button_layout.setContentsMargins(QMargins(20, 10, 20, 10))
        buttons = QWidget(self)
        buttons.setLayout(button_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(label, alignment=Qt.AlignCenter)
        layout.addWidget(buttons, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.show()