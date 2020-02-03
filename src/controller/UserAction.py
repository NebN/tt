from enum import Enum


class UserAction(Enum):
    SAVE = 'save'
    SAVE_AS = 'save as'
    OPEN = 'open'
    INFO = 'info'

    def __init__(self, label):
        self.label = label
