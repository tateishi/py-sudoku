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
