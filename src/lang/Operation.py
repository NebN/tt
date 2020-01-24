import re
from abc import abstractmethod
from src.model import Text
from .ast import Number
from .Transformation import Transformation


class Operation(Transformation):
    def __init__(self, pattern, operator):
        self.pattern = pattern.value()
        self.regex = re.compile(self.pattern)
        self.operator = operator

    def _operate_on_line(self, line):
        search = self.regex.search(line)

        if search is not None:
            match = search.group(0)
            op_res = self.operator.run(match)
            return line.replace(match, str(op_res), 1)

        return line

    def transform(self, text):
        lines = list(map(lambda l: self._operate_on_line(l), text.lines()))
        return Text(lines=lines)

    def __repr__(self):
        return f'{self.operator} to {self.pattern}'


class Operator:
    @abstractmethod
    def run(self, text):
        pass


class Add(Operator):
    def __init__(self, number):
        self.number = number

    def run(self, text):
        return Number(string=text).add(self.number)

    def __repr__(self):
        return f'Add {self.number}'


class Sub(Operator):
    def __init__(self, number):
        self.number = number

    def run(self, text):
        return Number(string=text).sub(self.number)

    def __repr__(self):
        return f'Sub {self.number}'

class Times(Operator):
    def __init__(self, number):
        self.number = number

    def run(self, text):
        return Number(string=text).times(self.number)

    def __repr__(self):
        return f'Times {self.number}'

class Divide(Operator):
    def __init__(self, number):
        self.number = number

    def run(self, text):
        return Number(string=text).divide(self.number)

    def __repr__(self):
        return f'Divide {self.number}'
