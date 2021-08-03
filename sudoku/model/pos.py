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

    @classmethod
    def from_xy(cls, x: int, y: int) -> Pos:
        return Pos(x + y * 9)
