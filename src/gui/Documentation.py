import os
import glob
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QTabWidget
from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtGui import QFont
from src import PRJ_ROOT


class Documentation(QDialog):
    def __init__(self, master=None):
        QDialog.__init__(self, master)
        self.setWindowModality(Qt.NonModal)
        self.setWindowTitle('Info')
        self.tabs = QTabWidget(self)
        self.tabs.setTabsClosable(False)
        margins = QMargins(10, 5, 10, 5)
        font = QFont()
        font.setPointSize(10)

        for filename in glob.glob(os.path.join(*[PRJ_ROOT, 'res', 'docs'], '*.txt')):
            with open(filename) as doc:
                label = QLabel(self)
                label.setContentsMargins(margins)
                label.setFont(font)
                label.setText(doc.read())
                self.tabs.addTab(label, os.path.basename(filename)[:-4])

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.show()
