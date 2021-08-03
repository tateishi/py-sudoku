from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Pos:
    idx: int

    @property
    def x(self) -> int:
        return self.idx % 9

    @property
    def y(self) -> int:
        return self.idx // 9

    @property
    def blk(self) -> int:
        r = self.idx // 27
        c0 = self.idx % 9
        c = c0 // 3
        return r * 3 + c

    def __str__(self):
        return str(self.idx)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, int):
            return self.idx == other
        elif isinstance(other, Pos):
            return self.idx == other
        else:
            raise NotImplemented

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @classmethod
    def from_xy(cls, x: int, y: int) -> Pos:
        return Pos(x + y * 9)
