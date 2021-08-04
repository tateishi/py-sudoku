from __future__ import annotations
from typing import List
from dataclasses import dataclass

#from ..model import Pos


@dataclass
class SingleCandidate:
    pos: Pos
    number: int
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.pos.idx}, {self.number}'


@dataclass
class MultiCandidate:
    pos: List[int]
    number: List[int]
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.pos}, {self.number}'


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
            return set()

    def __setitem__(self, key, value):
        if key in self.dict:
            self.dict[key].add(value)
        else:
            self.dict[key] = set((value,))

    def __str__(self):
        return str(self.dict)
