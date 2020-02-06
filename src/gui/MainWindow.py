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

        self.tabs = TabWidget(self)
        self.tabs.emptied.connect(lambda x: self.close())
        layout.addWidget(self.tabs)

    def closeEvent(self, event):
        if self.tabs.safeclose():
            event.accept()
        else:
            event.ignore()
