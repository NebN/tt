from rply import LexerGenerator


class Lexer:
    def __init__(self):
        self.lexer = LexerGenerator()

    def get_lexer(self):
        # elements
        self.lexer.add('STRING', r'''"[^"\\]*(\\.[^"\\]*)*"''')
        self.lexer.add('NUMBER', '[\d\.\,]+')
        self.lexer.add('FLAGS', '-[a-zA-Z]+')

        # transformations
        self.lexer.add('REPLACE', 'replace')
        self.lexer.add('WITH', 'with')
        self.lexer.add('SORT', 'sort')
        self.lexer.add('DISTINCT', 'distinct')
        self.lexer.add('GREP', 'grep')
        self.lexer.add('JOIN', 'join')
        self.lexer.add('SPLIT', 'split')

        # operations
        self.lexer.add('ADD', '\+')
        self.lexer.add('SUB', '-')
        self.lexer.add('TIMES', '\*')
        self.lexer.add('DIVIDE', '/')

        self.lexer.add('AS', 'as')

        # ignore
        self.lexer.ignore('\s+')
        self.lexer.ignore('\s*//.*')  # comments start with '//'
        self.lexer.ignore('\s*--.*')  # or '--'

        return self.lexer.build()
