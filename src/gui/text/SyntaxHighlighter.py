from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont, QColor
from PyQt5.QtCore import QRegExp
from lang import Pattern


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, editor):
        QSyntaxHighlighter.__init__(self, editor.document())
        self.base_format = self.format(0)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor('#FDFEFE'))
        keyword_format.setFontWeight(QFont.Bold)

        string_format = QTextCharFormat()
        string_format.setForeground(QColor('#DAF7A6'))

        flags_format = QTextCharFormat()
        flags_format.setForeground(QColor('#FFC300'))

        indices_format = QTextCharFormat()
        indices_format.setForeground(QColor('#BBE0FE'))

        comment_format = QTextCharFormat()
        comment_color = QColor('#FDF2E9')
        comment_color.setAlpha(80)
        comment_format.setForeground(comment_color)

        self.rules = []

        # strings
        self.rules.append((Pattern.STRING.pattern, string_format))

        # comments
        self.rules.append((Pattern.SLASH_COMMENT.pattern, comment_format))
        self.rules.append((Pattern.DASH_COMMENT.pattern, comment_format))

        # flags
        self.rules.append((Pattern.FLAGS.pattern, flags_format))

        # indices
        self.rules.append((Pattern.INDICES.pattern, indices_format))

        # keywords
        for word in Pattern.keywords():
            regex = QRegExp(fr'\b{word}\b')
            self.rules.append((regex, keyword_format))

    def highlightBlock(self, text):
        for pattern, font in self.rules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                # do not change formatting twice
                if self.format(index) == self.base_format:
                    self.setFormat(index, length, font)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
