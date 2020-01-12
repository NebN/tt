from rply import ParserGenerator
from .ast import String, ReplaceWith, Procedure


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            ['STRING', 'REPLACE', 'WITH']
        )

    def parse(self):
        @self.pg.production('operation : REPLACE STRING WITH STRING')
        def replace_with(p):
            original = String(p[1].value)
            replacement = String(p[3].value)
            return ReplaceWith(original, replacement)

        @self.pg.production('operation : operation\noperation')
        def operations(p):
            first = p[0]
            second = p[1]
            return Procedure(first, second)




        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
