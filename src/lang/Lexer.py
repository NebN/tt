from rply import LexerGenerator
from .patterns import *


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def get_lexer(self):
        # elements
        self.lexer.add('STRING', STRING)
        self.lexer.add('NUMBER', NUMBER)
        self.lexer.add('FLAGS', FLAGS)

        # transformations
        self.lexer.add('REPLACE', REPLACE)
        self.lexer.add('WITH', WITH)
        self.lexer.add('SORT', SORT)
        self.lexer.add('DISTINCT', DISTINCT)
        self.lexer.add('GREP', GREP)
        self.lexer.add('JOIN', JOIN)
        self.lexer.add('SPLIT', SPLIT)

        # operations
        self.lexer.add('ADD', ADD)
        self.lexer.add('SUB', SUB)
        self.lexer.add('TIMES', TIMES)
        self.lexer.add('DIVIDE', DIVIDE)

        self.lexer.add('AS', AS)

        # ignore
        self.lexer.ignore('\s+')
        self.lexer.ignore(SLASH_COMMENT)
        self.lexer.ignore(DASH_COMMENT)

        return self.lexer.build()
