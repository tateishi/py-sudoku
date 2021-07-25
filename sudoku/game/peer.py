from __future__ import annotations
from dataclasses import dataclass

from .pos import Pos


@dataclass
class Peer:
    peer: Set[Pos]

    def __str__(self):
        return f'[{",".join(str(p) for p in sorted(self.peer))}]'

    def __or__(self, p):
        return Peer(self.peer | p.peer)

    def __and__(self, p):
        return Peer(self.peer & p.peer)

    def __contains__(self, n: int) -> bool:
        return n in self.peer

    def __len__(self) -> int:
        return len(self.peer)

    @classmethod
    def col(cls, p) -> Peer:
        if isinstance(p, int):
            return Peer({i * 9 + p for i in range(9)})
        elif isinstance(p, Pos):
            return Peer.col(p.x)
        else:
            raise TypeError

    @classmethod
    def row(cls, p) -> Peer:
        if isinstance(p, int):
            return Peer({p * 9 + i for i in range(9)})
        elif isinstance(p, Pos):
            return Peer.row(p.y)
        else:
            raise TypeError

    @classmethod
    def blk(cls, p) -> Peer:
        if isinstance(p, int):
            r = p // 3
            c = p % 3
            b = r * 27 + c * 3
            return Peer({b + i for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)})
        elif isinstance(p, Pos):
            return Peer.blk(p.blk)
        else:
            raise TypeError

    @classmethod
    def peers(cls ,p: Pos) -> Peer:
        return Peer.col(p) | Peer.row(p) | Peer.blk(p)
