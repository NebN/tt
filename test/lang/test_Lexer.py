import os
import unittest

from rply import Token

from src.lang.Lexer import Lexer


class LexerTest(unittest.TestCase):

    lexer = Lexer().get_lexer()

    def test_single_keyword(self):
        tokens = list(self.lexer.lex('replace'))
        assert(tokens[0] == Token('REPLACE', 'replace'))

    def test_transformation(self):
        tokens = list(self.lexer.lex('replace "one" with "two"'))
        assert(tokens[0] == Token('REPLACE', 'replace'))
        assert(tokens[1] == Token('STRING', '"one"'))
        assert(tokens[2] == Token('WITH', 'with'))
        assert(tokens[3] == Token('STRING', '"two"'))

    def test_flags(self):
        tokens = list(self.lexer.lex('grep -vi "one"'))
        assert(tokens[0] == Token('GREP', 'grep'))
        assert(tokens[1] == Token('FLAGS', '-vi'))
        assert(tokens[2] == Token('STRING', '"one"'))

    def test_newline(self):
        tokens = list(self.lexer.lex(os.linesep))
        assert(tokens[0] == Token('NEWLINE', '\n'))

    def test_whitespace(self):
        tokens = list(self.lexer.lex('   '))
        assert(not tokens)

    def test_multi_transformation(self):
        tokens = list(self.lexer.lex('''replace "one" with "two"
        grep "three"'''))
        assert(tokens[0] == Token('REPLACE', 'replace'))
        assert(tokens[1] == Token('STRING', '"one"'))
        assert(tokens[2] == Token('WITH', 'with'))
        assert(tokens[3] == Token('STRING', '"two"'))
        assert(tokens[4] == Token('NEWLINE', '\n'))
        assert(tokens[5] == Token('GREP', 'grep'))
        assert(tokens[6] == Token('STRING', '"three"'))
