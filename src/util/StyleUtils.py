import re
from PyQt5.QtGui import QColor

def change_property(stylesheet, name, value):
    properties = stylesheet.split(';')
    changed = False

    for ix, p in enumerate(properties):
        if re.search(f'{name}\s*:', p):
            properties[ix] = f'{name}: {value}'
            changed = True
            break

    joined = ';'.join(properties)

    if changed:
        return joined
    else:
        return joined + f'\n{name}: {value};'


def get_property(stylesheet, name):
    for p in stylesheet.split(';'):
        if re.search(f'{name}\s*:', p):
            return re.sub(f'{name}\s*:', '', p).strip()


def color_as_css(color):
    return f'rgba({color.red()},{color.green()},{color.blue()},{color.alpha()})'


def css_as_color(css):
    red, green, blue, alpha = css[5:-1].split(',')
    return QColor(int(red), int(green), int(blue), int(alpha))
