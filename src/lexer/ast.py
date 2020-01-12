import re
from abc import abstractmethod
from src.model import Text


class String:
    def __init__(self, value):
        self._value = re.match('"(.*)"', value).group(1)

    def value(self):
        return self._value


class Transformation:
    @abstractmethod
    def transform(self, text):
        pass


class Replace(Transformation):
    def __init__(self, original, replacement):
        self.original = original.value()
        self.replacement = replacement.value()

    def transform(self, text):
        return Text(text=text.text().replace(self.original, self.replacement))

    def __repr__(self):
        return f'Replace {self.original} with {self.replacement}'

class Sort(Transformation):
    def __init__(self, reverse):
        self.reverse = reverse

    def transform(self, text):
        lines = text.lines()
        lines.sort(reverse=self.reverse)
        return Text(lines=lines)

    def __repr__(self):
        return f'Sort reverse={self.reverse}'


class MultiTransformation(Transformation):
    def __init__(self, *transformations):
        self.transformations = transformations

    def transform(self, text):
        transformed = text
        for t in self.transformations:
            transformed = t.transform(transformed)
        return transformed

    def __repr__(self):
        return "\n".join([str(t) for t in self.transformations])

