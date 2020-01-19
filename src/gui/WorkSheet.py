from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, pyqtSignal, QMargins
from PyQt5.QtGui import QFont
from .TextArea import TextArea


class WorkSheet(QWidget):

    run = pyqtSignal(str)

    def __init__(self, master=None):
        QWidget.__init__(self, master)
        self.code = TextArea(self)
        self.input = TextArea(self)
        self.output = TextArea(self)
        self.output.setReadOnly(True)
        self.message = QLabel('.* hello .*')
        messagefont = QFont()
        messagefont.setPointSize(9)
        self.message.setFont(messagefont)

        toplayout = QVBoxLayout(self)
        toplayout.setContentsMargins(QMargins(0, 0, 0, 0))
        toplayout.addWidget(self.message, alignment=Qt.AlignCenter)
        toplayout.addWidget(self.code)
        topwidget = QWidget()
        topwidget.setLayout(toplayout)

        vsplitter = QSplitter(Qt.Horizontal)
        vsplitter.addWidget(self.input)
        vsplitter.addWidget(self.output)

        hsplitter = QSplitter(Qt.Vertical)
        hsplitter.addWidget(topwidget)
        hsplitter.addWidget(vsplitter)
        hsplitter.setStretchFactor(0, 1)
        hsplitter.setStretchFactor(1, 8)

        layout = QVBoxLayout(self)
        layout.addWidget(hsplitter)

        self.code.keyPressed.connect(self._handlepress)

        self.setLayout(layout)

        self.input.set('some text for testing purposes\n'
                        'This Is All Capitalized')
        self.code.set('replace "\w+" with "asd"')

    def _handlepress(self, event):
        if event.key() == Qt.Key_Return and event.modifiers() == Qt.ControlModifier:
            self.run.emit(self.code.get())

    def setoutput(self, text):
        return self.output.set(text)

    def getinput(self):
        return self.input.get()

    def setmessage(self, message):
        self.message.setText(message)
