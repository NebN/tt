import os
import re
from functools import reduce
from abc import abstractmethod
from more_itertools import unique_everseen
from src.model import Text


class Transformation:
    @abstractmethod
    def transform(self, text):
        pass


class Replace(Transformation):
    def __init__(self, original, replacement):
        self.original = original.value()
        self.replacement = replacement.value()

    def transform(self, inputtext):
        return Text(text=re.sub(self.original, self.replacement, inputtext.text()))

    def __repr__(self):
        return f'Replace {self.original} with {self.replacement}'


class Sort(Transformation):
    def __init__(self, flags):
        self.flags = flags

    def transform(self, text):
        lines = text.lines()
        lines.sort(reverse=self.flags.exists('r'))
        return Text(lines=lines)

    def __repr__(self):
        return f'Sort {self.flags}'


class Distinct(Transformation):
    def transform(self, text):
        lines = text.lines()
        lines = unique_everseen(lines)
        return Text(lines=list(lines))

    def __repr__(self):
        return 'Distinct'


class Grep(Transformation):
    def __init__(self, pattern, flags):
        self.pattern = pattern.value()
        self.flags = flags

    def transform(self, text):
        regex_flags = [Grep._interpret_flag(f) for f in self.flags.all()]
        regex_flags.append(0)
        regex = re.compile(self.pattern, flags=reduce(lambda a, b: a | b, regex_flags))
        lines = text.lines()

        exact = self.flags.exists('o')
        invert = self.flags.exists('v')

        match = regex.match if exact else regex.search

        def keep(line):
            return (match(line) is not None) != invert

        result = [line for line in lines if keep(line)]

        return Text(lines=result)

    @classmethod
    def _interpret_flag(cls, flag):
        if flag == 'i':
            return re.IGNORECASE
        if flag == 'm':
            return re.MULTILINE
        return 0

    def __repr__(self):
        return f'Grep {self.pattern} {self.flags}'


class Join(Transformation):
    def __init__(self, string=None):
        self.string = string.value() if string else ', '

    def transform(self, text):
        return Text(text=self.string.join(text.lines()))

    def __repr__(self):
        return f'Join {self.string}'


class Split(Transformation):
    def __init__(self, string):
        self.string = string.value()

    def transform(self, text):
        return Text(text=re.sub(self.string, os.linesep, text.text()))

    def __repr__(self):
        return f'Split {self.string}'


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
