import re


class String:
    def __init__(self, value):
        self.value = re.match('"(.*)"', value).group(1)

    def eval(self):
        return self.value


class ReplaceWith:
    def __init__(self, original, replacement):
        def replace(string):
            print(f'replacing {original.eval()} with {replacement.eval()} in {string}')
            return string.replace(original.eval(), replacement.eval())

        self.f = replace

    def eval(self):
        return self.f


class Procedure:
    def __init__(self, a, b):
        def combine(string):
            return b.eval()(a.eval()(string))

        self.f = combine

    def eval(self):
        return self.f
