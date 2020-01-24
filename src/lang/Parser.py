from rply import ParserGenerator
from .ast import String, Number, Flags
from .Transformation import Replace, Sort, Distinct, Grep, Join, Split, MultiTransformation
from .Operation import Operation, Add, Sub, Times, Divide


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            ['STRING', 'NUMBER', 'FLAGS',
             'REPLACE', 'WITH', 'SORT', 'DISTINCT', 'GREP', 'JOIN', 'SPLIT',
             'ADD', 'SUB', 'TIMES', 'DIVIDE', 'AS']
        )

    def parse(self):
        @self.pg.production('transformation : REPLACE string WITH string')
        def replace_with(p):
            original = p[1]
            replacement = p[3]
            return Replace(original, replacement)

        @self.pg.production('transformation : GREP string')
        @self.pg.production('transformation : GREP flags string')
        def distinct(p):
            pattern = p[-1]
            flags = p[1] if len(p) == 3 else Flags.empty()
            return Grep(pattern, flags)

        @self.pg.production('transformation : SORT')
        @self.pg.production('transformation : SORT flags')
        def sort(p):
            flags = p[1] if len(p) == 2 else Flags.empty()
            return Sort(flags)

        @self.pg.production('transformation : DISTINCT')
        def distinct(_):
            return Distinct()

        @self.pg.production('transformation : JOIN')
        @self.pg.production('transformation : JOIN string')
        def join(p):
            if len(p) > 1:
                return Join(string=p[1])
            else:
                return Join()

        @self.pg.production('transformation : SPLIT string')
        def split(p):
            return Split(string=p[1])

        @self.pg.production('transformation : string ADD number')
        @self.pg.production('transformation : string SUB number')
        @self.pg.production('transformation : string TIMES number')
        @self.pg.production('transformation : string DIVIDE number')
        def arithmetic_operation(p):
            pattern = p[0]
            amount = p[2]
            tokentype = p[1].gettokentype()
            if tokentype == 'ADD':
                return Operation(pattern=pattern, operator=Add(amount))
            elif tokentype == 'SUB':
                return Operation(pattern=pattern, operator=Sub(amount))
            elif tokentype == 'TIMES':
                return Operation(pattern=pattern, operator=Times(amount))
            else:
                return Operation(pattern=pattern, operator=Divide(amount))

        @self.pg.production('transformation : transformation transformation')
        def multi(p):
            first = p[0]
            second = p[1]
            return MultiTransformation(first, second)

        @self.pg.production('string : STRING')
        def string(p):
            return String(p[0].value)

        @self.pg.production('number : NUMBER')
        def number(p):
            return Number(string=p[0].value)

        @self.pg.production('flags : FLAGS')
        def flags(p):
            return Flags(p[0].value)

        @self.pg.error
        def error_handle(token):
            print(f'unexpected {token.gettokentype()} token ({token.getstr()})')
            raise ValueError(token)

    def get_parser(self):
        return self.pg.build()
