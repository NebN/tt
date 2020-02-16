import re
import itertools
from .Lexer import Lexer
from .Parser import Parser
from .Pattern import Pattern

_lexer = Lexer().get_lexer()
pg = Parser()
pg.parse()
parser = pg.get_parser()


def compile_transformation(code):
    _tokens, _tokens2 = itertools.tee(_lexer.lex(code))
    transformation = parser.parse(_tokens)
    print(transformation)
    return transformation
