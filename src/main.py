from src.lexer.Lexer import Lexer
from src.lexer.Parser import Parser
from src.model import Text

text = Text(text="""
lmao " lol kek
xddd lmao
wtf lol
kek asd lmao xd
""")

code = """
replace "lmao" with "what??" 
replace "lol" with "kek" 
replace "kek" with "lmao"
sort    reverse          replace "??" with "!!!!!"
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
