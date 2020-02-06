from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import Qt, QRegExp


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, editor):
        QSyntaxHighlighter.__init__(self, editor.document())
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('#FDFEFE'))
        keyword_format.setFontWeight(QFont.Bold)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor('#DAF7A6'))

        keywords = ['replace', 'with', 'sort', 'grep', 'distinct', 'join', 'split']

        self.rules = []

        # strings
        self.rules.append(('\".*\"', string_format))

        # keywords
        for word in keywords:
            regex = QRegExp(f'\\b{word}\\b')
            self.rules.append((regex, keyword_format))

    def highlightBlock(self, text):
        for pattern, font in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, font)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
