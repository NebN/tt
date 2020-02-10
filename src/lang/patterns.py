STRING = r'''"[^"\\]*(\\.[^"\\]*)*"'''
NUMBER = r'''[\d\.\,]+'''
FLAGS = r'''-[a-zA-Z]+'''

REPLACE = r'replace'
WITH = r'with'
SORT = r'sort'
DISTINCT = r'distinct'
GREP = r'grep'
JOIN = r'join'
SPLIT = r'split'
AS = r'as'

ADD = r'\+'
SUB = r'-'
TIMES = r'\*'
DIVIDE = r'/'

SLASH_COMMENT = r'//[^\n]*'
DASH_COMMENT = r'--[^\n]*'

KEYWORDS = [
    REPLACE,
    WITH,
    SORT,
    DISTINCT,
    GREP,
    JOIN,
    SPLIT,
    AS
]
