from rply import ParserGenerator
from .ast import String, Number, Flags, Indices
from .Transformation import *
from .Operation import Operation, Add, Sub, Times, Divide
from .Pattern import Pattern


class Parser:
    def __init__(self):
        self.pg = ParserGenerator(
            [label for label in Pattern.labels() if 'COMMENT' not in label],
            precedence=[
                ('left', Pattern.keywords()),
                ('left', [Pattern.FLAGS.label, Pattern.INPUT_TYPE.label, Pattern.INDICES.label]),
                ('left', [Pattern.TIMES.label, Pattern.DIVIDE.label]),
                ('left', [Pattern.ADD.label, Pattern.SUB.label]),
                ('left', [Pattern.STRING.label, Pattern.NUMBER.label])
            ]
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
            flgs = p[1] if len(p) == 3 else Flags.empty()
            return Grep(pattern, flgs)

        @self.pg.production('transformation : SORT')
        @self.pg.production('transformation : SORT flags')
        def sort(p):
            flgs = p[1] if len(p) == 2 else Flags.empty()
            return Sort(flgs)

        @self.pg.production('transformation : DISTINCT')
        def distinct(_):
            return Distinct()

        @self.pg.production('transformation : JOIN')
        @self.pg.production('transformation : JOIN string')
        @self.pg.production('transformation : JOIN string string string')
        def join(p):
            if len(p) == 1:
                return Join()
            if len(p) == 2:
                return Join(middle=p[1])
            else:
                return Join(left=p[1], middle=p[2], right=p[3])

        @self.pg.production('transformation : SPLIT string')
        def split(p):
            return Split(string=p[1])

        @self.pg.production('transformation : STRIP')
        @self.pg.production('transformation : STRIP flags')
        def strip(p):
            flgs = p[1] if len(p) == 2 else Flags.empty()
            return Strip(flgs)

        @self.pg.production('transformation : UPPER string')
        def upper(p):
            return GroupsTransformation(p[1], lambda s: s.upper())

        @self.pg.production('transformation : LOWER string')
        def lower(p):
            return GroupsTransformation(p[1], lambda s: s.lower())

        @self.pg.production('transformation : FORMAT input_type')
        @self.pg.production('transformation : FORMAT input_type')
        def form(p):
            return Format(p[1])

        @self.pg.production('transformation : KEEP indices')
        def keep(p):
            return Keep(indices=p[1])

        @self.pg.production('transformation : REMOVE indices')
        def remove(p):
            return Remove(indices=p[1])

        @self.pg.production('transformation : CUT string KEEP indices')
        def cut(p):
            return Cut(separator=p[1], fields_to_keep=p[3])

        @self.pg.production('transformation : PREPEND string')
        @self.pg.production('transformation : PREPEND flags string')
        @self.pg.production('transformation : APPEND string')
        @self.pg.production('transformation : APPEND flags string')
        def prepend(p):
            tokentype = p[0].gettokentype()
            flgs = p[1] if len(p) == 3 else Flags.empty()
            if tokentype == 'PREPEND':
                print('PREPEND')
                return AddText(add=lambda s: f'{p[-1]}{s}', flags=flgs)
            elif tokentype == 'APPEND':
                print('APPEND')
                return AddText(add=lambda s: f'{s}{p[-1]}', flags=flgs)

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

        @self.pg.production('transformation : transformation newlines transformation')
        def multi(p):
            return MultiTransformation(p[0], p[2])

        @self.pg.production('newlines : NEWLINE')
        @self.pg.production('newlines : newlines NEWLINE')
        def newlines(p):
            return p[0]

        @self.pg.production('transformation : transformation newlines')
        def end(p):
            return p[0]

        @self.pg.production('string : STRING')
        def string(p):
            return String(p[0].value)

        @self.pg.production('number : NUMBER')
        def number(p):
            return Number(string=p[0].value)

        @self.pg.production('flags : FLAGS')
        def flags(p):
            return Flags(p[0].value)

        @self.pg.production('input_type : INPUT_TYPE')
        def input_type(p):
            for t in InputType:
                if p[0].value.upper() == t.label:
                    return t

        @self.pg.production('indices : INDICES')
        def indices(p):
            return Indices(p[0].value)

        @self.pg.error
        def error_handle(token):
            print(f'unexpected {token.gettokentype()} token ({token.getstr()})')
            if token.gettokentype() == '$end':
                raise ValueError('unexpected end of statement')
            else:
                raise ValueError(f'unexpected {token.getstr()}')

    def get_parser(self):
        return self.pg.build()
