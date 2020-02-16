from rply import LexerGenerator
from .Pattern import Pattern


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def get_lexer(self):
        for pattern in Pattern:
            if 'COMMENT' not in pattern.label:
                self.lexer.add(pattern.label, pattern.pattern)
            else:
                self.lexer.ignore(pattern.pattern)

        # ignore whitespace
        self.lexer.ignore(r'[ \t\r\f\v]+')

        return self.lexer.build()
