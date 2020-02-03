import os
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QMargins
from PyQt5.QtGui import QFont
from .TextArea import TextArea


class WorkSheet(QWidget):
    run = pyqtSignal(str)
    dirty = pyqtSignal(bool)
    name = pyqtSignal(str)

    def __init__(self, master=None):
        QWidget.__init__(self, master)
        self._filename = None
        self._savedtext = None
        self.isdirty = False
        self.code = TextArea(self)
        self.input = TextArea(self)
        self.output = TextArea(self)
        self.output.setReadOnly(True)
        self.message = QLabel('.* hello .*')
        messagefont = QFont()
        messagefont.setPointSize(9)
        self.message.setFont(messagefont)

        self.code.setMinimumSize(300, 65)
        self.code.textChanged.connect(self._handle_textchanged)

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
        hsplitter.setStretchFactor(1, 9)

        layout = QVBoxLayout(self)
        layout.addWidget(hsplitter)

        self.code.keyPressed.connect(self._handle_press)
        self.dirty.connect(self._handle_dirty)

        self.setLayout(layout)

    @staticmethod
    def from_file(filename, master=None):
        with open(filename) as file:
            code = file.read()
            ws = WorkSheet(master)
            ws.code.set(code)
            ws._savedtext = code
            ws._filename = filename
            ws.setdirty(False)
            return ws

    def setdirty(self, dirty):
        self.isdirty = dirty
        self.dirty.emit(self.isdirty)

    def setfilename(self, filename):
        self._filename = filename
        self.name.emit(os.path.basename(self._filename).split('.')[-2])

    def save(self, overwrite):
        if not self._filename or not overwrite:
            filename, _ = QFileDialog.getSaveFileName(None,
                                                      'Save the current transformation file',
                                                      '', 'TextTransformation (*.tt)')
            if filename:
                self.setfilename(filename)

        if self._filename and self.isdirty:
            self.setmessage('saving...')
            with open(self._filename, 'w+') as file:
                self._savedtext = self.code.get()
                file.write(self._savedtext)
                self.setdirty(False)
            self.setmessage(f'saved to {self._filename}')

    def _handle_dirty(self, dirty):
        if dirty:
            self.code.setStyleSheet('border: 1px solid red;')
        else:
            self.code.setStyleSheet('')

    def _handle_textchanged(self):
        self.setdirty(self._savedtext != self.code.get())

    def _handle_press(self, event):
        print("======================")
        print(event.modifiers() == Qt.ShiftModifier + Qt.ControlModifier)
        print(event.modifiers() == Qt.ControlModifier)
        print(event.modifiers() == Qt.AltModifier)
        print(event.modifiers() == Qt.MetaModifier)

        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Return:
                self.run.emit(self.code.get())
            elif event.key() == Qt.Key_S:
                self.save(overwrite=event.modifiers != Qt.ShiftModifier)

    def setoutput(self, text):
        return self.output.set(text)

    def getinput(self):
        return self.input.get()

    def setmessage(self, message):
        self.message.setText(message)
