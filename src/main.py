from tkinter import Tk, ttk
from src.lang.Lexer import Lexer
from src.lang.Parser import Parser
from src.model import Text
from src.gui import Window, SuperWindow
from src.controller import Controller

text = Text(text="""
lmao lol kek
xddd lmao
wtf lol
kek asd lmao xd
""")

code = """
replace "lmao" with "what??" 
replace "lol" with "kek" 
replace "kek" with "lmao"
sort    reverse          replace "\?\?" with "!!!!!"
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(code)

pg = Parser()
pg.parse()
parser = pg.get_parser()
transformation = parser.parse(tokens)
print(transformation)
print("==========================")
print(transformation.transform(text).text())

root = Tk()
root.style = ttk.Style()
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
root.style.theme_use('alt')
root.geometry('1000x600')

sw = SuperWindow(root)
sw.add_window("tabname")
sw.add_window("tabname2")
sw.add_window("tabname3")


root.mainloop()
