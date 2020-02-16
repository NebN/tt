import os
from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QMargins
from PyQt5.QtGui import QFont
from gui import Color
from gui.text import TextArea, SyntaxHighlighter


class WorkSheet(QWidget):
    run = pyqtSignal(str)
    dirty = pyqtSignal(bool)
    name = pyqtSignal(str)

    def __init__(self, master=None):
        QWidget.__init__(self, master)
        self._filename = None
        self._savedtext = None
        self.isdirty = False
        self.code = TextArea(self, pointsize=10)
        self.highlighter = SyntaxHighlighter(self.code)
        self.input = TextArea(self)
        self.output = TextArea(self)
        self.output.setReadOnly(True)
        self.message = QLabel('.* hello .*')
        messagefont = QFont()
        messagefont.setPointSize(9)
        self.message.setFont(messagefont)

        self.code.setMinimumSize(300, 65)
        self.code.set('sort')
        self.code.textChanged.connect(self._handle_code_textchanged)
        self.input.textChanged.connect(self._handle_input_textchanged)

        toplayout = QVBoxLayout(self)
        toplayout.setContentsMargins(QMargins(0, 0, 0, 0))
        toplayout.addWidget(self.message, alignment=Qt.AlignCenter)
        toplayout.addWidget(self.code)
        topwidget = QWidget(self)
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
        self.input.keyPressed.connect(self._handle_press)
        self.dirty.connect(self._handle_dirty)

        self.setLayout(layout)

        self.last_execution_code = ''

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
            self.code.flash(Color.BLUE)

    def _handle_dirty(self, dirty):
        if dirty:
            self.code.setbordercolor(Color.BLACK)
        else:
            self.code.setbordercolor(Color.DARK_BLUE)

    def _handle_code_textchanged(self):
        current_code = self.code.get()
        self.setdirty(current_code != self._savedtext)
        # For some reason pressing modifiers like CTRL or SHIFT triggers textChanged
        # so this check is necessary
        if current_code != self.last_execution_code:
            self.output.setbordercolor(Color.BLACK)

    def _handle_input_textchanged(self):
        self.output.setbordercolor(Color.BLACK)

    def _handle_press(self, event):
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
