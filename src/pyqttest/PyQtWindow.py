import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class QTest(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(900, 600))
        self.setWindowTitle('TT - Text Transformations')

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QGridLayout(self)
        widget.setLayout(layout)

        label = QLabel('some label', self)
        label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(label, 0, 0)

        tabs = QTabWidget()
        tab1 = QWidget()
        tab2 = QWidget()
        tabs.resize(400, 400)

        tabs.addTab(tab1, "tab 1")
        tabs.addTab(tab2, "tab 2")

        tab1Layout = QVBoxLayout(self)
        tab1Layout.addWidget(QPushButton('push batton'))
        tab1.setLayout(tab1Layout)

        layout.addWidget(tabs)

        def add_tab(e):
            print('adding tab')

        plusBatton = QPushButton('+')
        tabs.setCornerWidget(plusBatton)
        plusBatton.clicked.connect(add_tab)



app = QtWidgets.QApplication(sys.argv)
window = QTest()
window.show()
sys.exit(app.exec_())
