import unittest
from src.lang.Transformation import Replace
from src.lang.ast import String
from src.model import Text


class TransformationTest(unittest.TestCase):

    def test_dollarsign_groups(self):
        rep = Replace(String('"(one)"'), String('"two -> $1"'))
        res = rep.transform(Text(text='one two'))
        assert (res.text() == 'two -> one two')

    def test_escaped_dollarsign_groups(self):
        rep = Replace(String('"(one)"'), String(r'''"two -> \$1"'''))
        res = rep.transform(Text(text='one two'))
        assert (res.text() == r'''two -> \$1 two''')
