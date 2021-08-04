from __future__ import annotations
from dataclasses import dataclass

from .place import Place
from .grid import Grid


@dataclass(frozen=True)
class Peer:
    peer: set[int]

    def __str__(self):
        return f'[{",".join(str(p) for p in sorted(self.peer))}]'

    def __or__(self, p: Peer) -> Peer:
        return Peer(self.peer | p.peer)

    def __and__(self, p: Peer) -> Peer:
        return Peer(self.peer & p.peer)

    def __contains__(self, n: int | Grid) -> bool:
        if isinstance(n, int):
            return n in self.peer
        elif isinstance(n, Grid):
            return n.i in self.peer
        else:
            raise NotImplementedError

    def __len__(self) -> int:
        return len(self.peer)

    @classmethod
    def col(cls, p: int | Place) -> Peer:
        if isinstance(p, int):
            return cls({i * 9 + p for i in range(9)})
        elif isinstance(p, Place):
            return cls.col(p.x)
        else:
            raise TypeError

    @classmethod
    def row(cls, p: int | Place) -> Peer:
        if isinstance(p, int):
            return cls({p * 9 + i for i in range(9)})
        elif isinstance(p, Place):
            return cls.row(p.y)
        else:
            raise TypeError

    @classmethod
    def blk(cls, p: int | Place) -> Peer:
        if isinstance(p, int):
            r = p // 3
            c = p % 3
            b = r * 27 + c * 3
            return cls({b + i for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)})
        elif isinstance(p, Place):
            return cls.blk(p.b)
        else:
            raise TypeError

    @classmethod
    def peers(cls, p: Place) -> Peer:
        return cls.col(p) | cls.row(p) | cls.blk(p)
