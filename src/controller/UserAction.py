from enum import Enum


class UserAction(Enum):
    SAVE = 'save'
    OPEN = 'open'
    INFO = 'info'

    def __init__(self, label):
        self.label = label
