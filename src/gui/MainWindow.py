from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QSizePolicy
from PyQt5.QtCore import QSize, Qt
from .TabWidget import TabWidget


class MainWindow(QMainWindow):
    def __init__(self, master=None):
        QMainWindow.__init__(self, master)
        self.setMinimumSize(QSize(900, 600))
        self.setWindowTitle('TT - Text Transformations')

        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QGridLayout()
        widget.setLayout(layout)
        layout.setAlignment(Qt.AlignCenter)

        tabs = TabWidget()
        layout.addWidget(tabs)
