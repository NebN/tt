from lexer.Lexer import Lexer
from lexer.Parser import Parser

text = """
lmao lol kek
"""

code = """
replace "lol" with "kek"
replace "kek" with "lmao"
"""

lexer = Lexer().get_lexer()
tokens = lexer.lex(code)

pg = Parser()
pg.parse()
parser = pg.get_parser()
f = parser.parse(tokens).eval()
print(f(text))
