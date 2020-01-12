from rply import ParserGenerator
from .ast import String, Replace, Sort, MultiTransformation


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            ['STRING', 'REPLACE', 'WITH', 'SORT']
        )

    def parse(self):
        @self.pg.production('transformation : REPLACE STRING WITH STRING')
        def replace_with(p):
            original = String(p[1].value)
            replacement = String(p[3].value)
            return Replace(original, replacement)

        @self.pg.production('transformation : SORT')
        def sort(p):
            return Sort(reverse=p[0].value.endswith('reverse'))

        @self.pg.production('transformation : transformation\ntransformation')
        def operations(p):
            first = p[0]
            second = p[1]
            return MultiTransformation(first, second)

        @self.pg.error
        def error_handle(token):
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
