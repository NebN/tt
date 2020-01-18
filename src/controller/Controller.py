from src import lang
from src.model import Text


class Controller:

    def __init__(self, window):
        self.window = window
        self.window.codeinput.bind('<Control-Return>', self.execute)
        self.window.left.bind('<Control-Return>', self.execute)

    def execute(self, event):
        print('executing')
        self.window.infostring.set('executing...')
        transformation = lang.compile_transformation(self.window.code())
        self.window.setoutput(transformation.transform(Text(text=self.window.inputtext())).text())
        self.window.infostring.set('done')
        return 'break'
