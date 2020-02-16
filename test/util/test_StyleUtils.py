import unittest
from PyQt5.QtGui import QColor
from src.util import StyleUtils


class StyleUtilsTest(unittest.TestCase):

    def test_change_property(self):
        original = '''border-color: rgba(248,255,6,255);'''
        changed = StyleUtils.change_property(original, 'border-color', StyleUtils.color_as_css(QColor(100, 150, 200, 255)))
        assert (changed == 'border-color: rgba(100,150,200,255);')

    def test_get_property(self):
        style = '''
        border-color: rgba(248,255,6,255);
        border: 1px solid;
        some-prop: some values;
        '''
        p = StyleUtils.get_property(style, 'border')
        assert (p == '1px solid')

    def test_css_as_color(self):
        style = 'rgba(248,255,6,255)'
        color = StyleUtils.css_as_color(style)
        assert (color == QColor(248, 255, 6, 255))
