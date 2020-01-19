import sys
import traceback
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QT_VERSION, qFatal
from src.gui import MainWindow

app = QApplication(sys.argv)

if QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        qFatal('')
sys.excepthook = excepthook

window = MainWindow()
window.show()
sys.exit(app.exec_())
