from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass

from . import Place, Cell


@dataclass
class Grid:
    place: Place
    cell: Cell

    def __sub__(self, n: int | Sequence[int]) -> Grid:
        return type(self)(self.place, self.cell - n)

    def from_number(self, number: int) -> Grid:
        return type(self)(self.place, Cell.from_number(number))

    def from_memo(self, memo: Sequence[int]) -> Grid:
        return type(self)(self.place, memo)

    @classmethod
    def unknown(cls, n: int) -> Grid:
        return cls(Place(n), Cell.unknown())

    @property
    def fixed(self):
        return self.cell.fixed

    @property
    def canfix(self) -> Bool:
        return self.cell.canfix

    @property
    def fixable(self) -> int | None:
        return self.cell.fixable

    @property
    def memo(self) -> set[int]:
        return self.cell.content

    @property
    def i(self):
        return self.place.i

    @property
    def x(self):
        return self.place.x

    @property
    def y(self):
        return self.place.y

    @property
    def b(self):
        return self.place.b
