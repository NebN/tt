from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def get_lexer(self):
        # symbols
        self.lexer.add('OPEN_PAREN', '\(')
        self.lexer.add('CLOSE_PAREN', '\)')

        # elements
        self.lexer.add('STRING', '".*?"')

        # operators
        self.lexer.add('REPLACE', 'replace')
        self.lexer.add('WITH', 'with')
        self.lexer.add('SORT', 'sort(\s+reverse)?')

        self.lexer.ignore('\s+')

        return self.lexer.build()
