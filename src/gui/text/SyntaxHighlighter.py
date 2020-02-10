from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import Qt, QRegExp
from lang import patterns


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, editor):
        QSyntaxHighlighter.__init__(self, editor.document())
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('#FDFEFE'))
        keyword_format.setFontWeight(QFont.Bold)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor('#DAF7A6'))
        flags_format = QTextCharFormat()
        flags_format.setForeground(QColor('#FFC300'))
        comment_format = QTextCharFormat()
        comment_color = QColor('#FDF2E9')
        comment_color.setAlpha(80)
        comment_format.setForeground(comment_color)

        self.rules = []

        # strings
        self.rules.append((patterns.STRING, string_format))

        # comments
        self.rules.append((patterns.SLASH_COMMENT, comment_format))
        self.rules.append((patterns.DASH_COMMENT, comment_format))

        # flags
        self.rules.append((patterns.FLAGS, flags_format))

        # keywords
        for word in patterns.KEYWORDS:
            regex = QRegExp(fr'\b{word}\b')
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
