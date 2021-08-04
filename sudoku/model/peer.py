from __future__ import annotations
from typing import Set
from dataclasses import dataclass

#from . import Pos


@dataclass(frozen=True)
class Peer:
    peer: Set[int]

    def __str__(self):
        return f'[{",".join(str(p) for p in sorted(self.peer))}]'

    def __or__(self, p: Peer) -> Peer:
        return Peer(self.peer | p.peer)

    def __and__(self, p: Peer) -> Peer:
        return Peer(self.peer & p.peer)

    def __contains__(self, n: int) -> bool:
        return n in self.peer

    def __len__(self) -> int:
        return len(self.peer)

    @classmethod
    def col(cls, p: int | Pos) -> Peer:
        if isinstance(p, int):
            return cls({i * 9 + p for i in range(9)})
        elif isinstance(p, Pos):
            return cls.col(p.x)
        else:
            raise TypeError

    @classmethod
    def row(cls, p: int | Pos) -> Peer:
        if isinstance(p, int):
            return cls({p * 9 + i for i in range(9)})
        elif isinstance(p, Pos):
            return cls.row(p.y)
        else:
            raise TypeError

    @classmethod
    def blk(cls, p: int | Pos) -> Peer:
        if isinstance(p, int):
            r = p // 3
            c = p % 3
            b = r * 27 + c * 3
            return cls({b + i for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)})
        elif isinstance(p, Pos):
            return cls.blk(p.blk)
        else:
            raise TypeError

    @classmethod
    def peers(cls, p: Pos) -> Peer:
        return cls.col(p) | cls.row(p) | cls.blk(p)
