import re
import ast
import enum
from decimal import Decimal


class String:
    def __init__(self, value):
        self._value = ast.literal_eval(value)

    def value(self):
        return self._value

    def __repr__(self):
        return self.value()


class Number:
    def __init__(self, string=None, value=None):
        assert (string is not None or value is not None)
        if value is not None:
            self._value = value
        else:
            possible_separators = [',', '.']
            last_symbol = next((c for c in string[::-1] if c in possible_separators), None)

            is_separator = False
            cleaned = string

            if last_symbol is not None:
                is_separator = string.count(last_symbol) == 1
                if is_separator:
                    possible_separators.remove(last_symbol)
                for s in possible_separators:
                    cleaned = cleaned.replace(s, '', -1)
                cleaned = cleaned.replace(last_symbol, '.')

            if is_separator:
                self._value = Decimal(cleaned)
            else:
                self._value = int(cleaned)

    def value(self):
        return self._value

    def add(self, other):
        return Number(value=self.value() + other.value())

    def sub(self, other):
        return Number(value=self.value() - other.value())

    def times(self, other):
        return Number(value=self.value() * other.value())

    def divide(self, other):
        return Number(value=self.value() / other.value())

    def __repr__(self):
        if isinstance(self._value, int):
            return str(self._value)
        else:
            return '{:f}'.format(self._value)


class Flags:
    def __init__(self, value):
        chars = re.match('-(\w*)', value).group(1) if value else ''
        self._flags = [char for char in chars]

    def exists(self, flag):
        return flag in self._flags

    def all(self):
        return self._flags

    def isempty(self):
        return not self._flags

    @classmethod
    def empty(cls):
        return Flags('-')

    def __repr__(self):
        return ",".join(self._flags)


class InputType(enum.Enum):
    XML = 'XML'
    JSON = 'JSON'

    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return self.label


class Indices:
    def __init__(self, string):
        self.indices = []
        for section in string.strip()[1:-1].split(','):
            section_split = section.split('-')
            for ix in range(int(section_split[0]), int(section_split[-1]) + 1):
                self.indices.append(ix)

        self.indices.sort()

    def __iter__(self):
        return iter(self.indices)

    def __repr__(self):
        return ', '.join([str(i) for i in self.indices])
