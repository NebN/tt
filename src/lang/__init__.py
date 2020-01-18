from .Lexer import Lexer
from .Parser import Parser

_lexer = Lexer().get_lexer()
pg = Parser()
pg.parse()
parser = pg.get_parser()


def compile_transformation(code):
    _tokens = _lexer.lex(code)
    transformation = parser.parse(_tokens)
    print(transformation)
    return transformation
