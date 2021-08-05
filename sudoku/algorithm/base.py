from __future__ import annotations
from dataclasses import dataclass

from ..model import Place


@dataclass
class SingleCandidate:
    place: Place
    number: int
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.place.i}, {self.number}'


@dataclass
class MultiCandidate:
    places: list[Place]
    number: list[int]
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.places}, {self.number}'


class AppendDict:
    def __init__(self):
        self.dict = dict()

    def append(self, key, value):
        if key in self.dict:
            self.dict[key].append(value)
        else:
            self.dict[key] = [value]

    def items(self):
        return self.dict.items()

    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return list()

    def __setitem__(self, key, value):
        if key in self.dict:
            self.dict[key].append(value)
        else:
            self.dict[key] = [value]

    def __str__(self):
        return str(self.dict)
