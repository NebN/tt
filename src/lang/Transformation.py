import os
import re
import json
import xml.dom.minidom
from functools import reduce
from abc import abstractmethod
from more_itertools import unique_everseen
from src.model import Text
from .ast import InputType


class Transformation:
    @abstractmethod
    def transform(self, text):
        pass


class Replace(Transformation):
    def __init__(self, original, replacement):
        self.original = original.value()
        self.replacement = re.sub(r'(?<!\\)\$(\d+)', r'\\\1', replacement.value())

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
    def __init__(self, left=None, middle=None, right=None):
        self.left = left.value() if left else ''
        self.middle = middle.value() if middle else ','
        self.right = right.value() if right else ''

    def transform(self, text):
        joined = self.middle.join(text.lines())
        return Text(text=f'{self.left}{joined}{self.right}')

    def __repr__(self):
        return f'Join {self.left} {self.middle} {self.right}'


class Split(Transformation):
    def __init__(self, string):
        self.string = string.value()

    def transform(self, text):
        replacement = f'{self.string}{os.linesep}'
        return Text(text=re.sub(self.string, replacement, text.text()))

    def __repr__(self):
        return f'Split {self.string}'


class Strip(Transformation):
    def __init__(self, flags):
        self.flags = flags

    def transform(self, text):
        vertical = self.flags.exists('v')
        horizontal = self.flags.exists('h')

        if not horizontal and not vertical:
            vertical = True
            horizontal = True

        if vertical and horizontal:
            return Text(lines=[line.strip() for line in text.lines() if line])
        elif vertical:
            return Text(lines=[line for line in text.lines() if line])
        elif horizontal:
            return Text(lines=[line.strip() for line in text.lines()])

    def __repr__(self):
        return f'Strip {self.flags}'


class AddText(Transformation):
    def __init__(self, add, flags):
        self.add = add
        self.flags = flags

    def transform(self, text):
        if self.flags.exists('l'):
            return Text(lines=[self.add(line) for line in text.lines()])
        else:
            return Text(text=self.add(text.text()))

    def __repr__(self):
        return f'AddText {self.add} {self.flags}'


class GroupsTransformation(Transformation):
    def __init__(self, lower, transformation):
        self.pattern = re.compile(lower.value())
        self.transformation = transformation

    def _transform_line_function(self):
        if self.pattern.groups:

            # if the pattern has groups transform only the sections that match
            def f(line):
                transformed = line
                search = self.pattern.search(line)
                if search:
                    for ix in range(1, len(search.groups()) + 1):
                        s, e = search.span(ix)
                        transformed = transformed[:s] + self.transformation(transformed[s:e]) + transformed[e:]
                return transformed

            return f

        # otherwise transform the entire section that matches the pattern
        else:

            def f(line):
                search = self.pattern.search(line)
                if search:
                    start, end = search.span()
                    return line[:start] + self.transformation(line[start:end]) + line[end:]
                else:
                    return line

            return f

    def transform(self, text):
        function = self._transform_line_function()
        return Text(lines=[function(line) for line in text.lines()])

    def __repr__(self):
        return f'GroupsTransformation {self.transformation.__name__} {self.pattern}'


class Format(Transformation):
    XML = 'XML'
    JSON = 'JSON'

    def __init__(self, input_type):
        self.input_type = input_type

    def transform(self, text):
        if self.input_type == InputType.XML:
            x = xml.dom.minidom.parseString(text.text())
            return Text(text=x.toprettyxml(indent='  '))
        elif self.input_type == InputType.JSON:
            j = json.loads(text.text())
            return Text(text=json.dumps(j, indent=2))

    def __repr__(self):
        return f'Format {self.input_type.label}'


class Keep(Transformation):
    def __init__(self, indices):
        self.indices = indices

    def transform(self, text):
        kept_lines = []
        for ix in self.indices:
            try:
                kept_lines.append(text.lines()[ix])
            except IndexError:
                pass
        return Text(lines=kept_lines)

    def __repr__(self):
        return f'Keep {self.indices}'


class Remove(Transformation):
    def __init__(self, indices):
        self.indices = indices

    def transform(self, text):
        kept_lines = text.lines()
        for ix in self.indices:
            try:
                del kept_lines[ix]
            except IndexError:
                pass
        return Text(lines=kept_lines)

    def __repr__(self):
        return f'Remove {self.indices}'


class Cut(Transformation):
    def __init__(self, separator, fields_to_keep):
        self.separator = separator.value()
        self.fields_to_keep = fields_to_keep

    def _keep_fields(self, fields):
        kept_fields = []
        for ix in self.fields_to_keep:
            try:
                kept_fields.append(fields[ix])
            except IndexError:
                pass
        return self.separator.join(kept_fields)

    def transform(self, text):
        lines = [self._keep_fields(line.split(self.separator)) for line in text.lines()]
        return Text(lines=lines)

    def __repr__(self):
        return f'Cut {self.separator} keep {self.fields_to_keep}'


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
