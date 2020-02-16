from enum import Enum


class Pattern(Enum):

    def __init__(self, label, pattern):
        self.label = label
        self.pattern = pattern

    @classmethod
    def labels(cls):
        return [p.label for p in cls]

    @classmethod
    def patterns(cls):
        return [p.pattern for p in cls]

    STRING = 'STRING', r'''"[^"\\]*(\\.[^"\\]*)*"'''
    NUMBER = 'NUMBER', r'''[\d\.]+'''

    FLAGS = 'FLAGS', r'''-[a-zA-Z]+'''
    INPUT_TYPE = 'INPUT_TYPE', r'''xml|XML|json|JSON'''
    INDICES = 'INDICES', r'''\[\s*\d+( *[,-] *\d+)*\]'''

    # keywords
    REPLACE = 'REPLACE', r'replace(?!\w)'
    WITH = 'WITH', r'with(?!\w)'
    SORT = 'SORT', r'sort(?!\w)'
    DISTINCT = 'DISTINCT', r'distinct(?!\w)'
    GREP = 'GREP', r'grep(?!\w)'
    JOIN = 'JOIN', r'join(?!\w)'
    SPLIT = 'SPLIT', r'split(?!\w)'
    # AS = 'AS', r'as(?!\w)'
    STRIP = 'STRIP', r'strip(?!\w)'
    LOWER = 'LOWER', r'lower(?!\w)'
    UPPER = 'UPPER', r'upper(?!\w)'
    # WHEN = 'WHEN', r'when(?!\w)'
    FORMAT = 'FORMAT', r'format(?!\w)'
    CUT = 'CUT', r'cut(?!\w)'
    KEEP = 'KEEP', r'keep(?!\w)'
    REMOVE = 'REMOVE', r'remove(?!\w)'
    APPEND = 'APPEND', r'append(?!\w)'
    PREPEND = 'PREPEND', r'prepend(?!\w)'

    # arithmetic operators
    ADD = 'ADD', r'\+'
    SUB = 'SUB', r'-'
    TIMES = 'TIMES', r'\*'
    DIVIDE = 'DIVIDE', r'/'

    # comments
    SLASH_COMMENT = 'SLASH_COMMENT', r'//[^\n]*'
    DASH_COMMENT = 'DASH_COMMENT', r'--[^\n]*'

    NEWLINE = 'NEWLINE', r'\n'

    @classmethod
    def keywords(cls):
        return [p.pattern for p in [
            cls.REPLACE,
            cls.WITH,
            cls.SORT,
            cls.DISTINCT,
            cls.GREP,
            cls.JOIN,
            cls.SPLIT,
            # cls.AS,
            cls.STRIP,
            cls.LOWER,
            cls.UPPER,
            # cls.WHEN,
            cls.FORMAT,
            cls.KEEP,
            cls.REMOVE,
            cls.CUT,
            cls.APPEND,
            cls.PREPEND
        ]]
