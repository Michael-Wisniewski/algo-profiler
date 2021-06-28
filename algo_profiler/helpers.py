from enum import Enum


class LabelBase(Enum):
    def __str__(self):
        return self.value
