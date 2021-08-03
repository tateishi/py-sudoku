from __future__ import annotations
from typing import List

from ..model import Pos, Peer, Cell, Sudoku
from . import MultiCandidate, AlgorithmDouble, AppendDict


class AlgorithmTuple(AlgorithmDouble):
    def __init__(self, sudoku: Sudoku, n: int, name: str):
        self.n = n
        self.name = name
        super().__init__(sudoku)

    def inclusive(self, c: Cell, s: set[int]) -> bool:
        return True

    def find_peer(self, peer: Peer, reason: str) -> List[MultiCandidate]:
        def reverse_dict(d: AppendDict, c: Cell, s: set[int]) -> AppendDict:
            if self.inclusive(c, s):
                d[frozenset(s)] = c.pos.idx
            return d


        from operator import or_
        from functools import reduce
        from itertools import combinations

        peers = [self.sudoku[p] for p in peer.peer
                 if not self.sudoku[p].cell.fixed]
        if len(peers) == 0: return list()
        memos = reduce(or_, (c.cell.memo for c in peers))
        sets = [set(s) for s in combinations(memos, self.n)]

        dict = AppendDict()
        for s in sets:
            for p in peers:
                dict = reverse_dict(dict, p, s)

        p0 = {p.pos.idx for p in peers}
        r = f'{self.name} on {reason}'
        candidates = [MultiCandidate(list(p0-v), list(k), r)
                      for k, v in dict.dict.items()
                      if len(v) == self.n]
        return candidates

    def find(self) -> List[MultiCandidate]:
        from operator import add
        from functools import reduce

        candidates = (
            [self.find_peer(Peer.col(n), f'col{n}') for n in range(9)] +
            [self.find_peer(Peer.row(n), f'row{n}') for n in range(9)] +
            [self.find_peer(Peer.blk(n), f'blk{n}') for n in range(9)]
        )

        return reduce(add, candidates)


class NakedTuple(AlgorithmTuple):
    def inclusive(self, c: Cell, s: set[int]) -> bool:
        return s >= c.cell.memo


class HiddenTuple(AlgorithmTuple):
    def inclusive(self, c: Cell, s: set[int]) -> bool:
        return bool(s & c.cell.memo)


class NakedDouble(NakedTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 2, 'naked double')


class HiddenDouble(HiddenTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 2, 'hidden double')


class NakedTriple(NakedTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 3, 'naked triple')


class HiddenTriple(HiddenTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 3, 'hidden triple')


class NakedQuadruple(NakedTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 4, 'naked quadruple')


class HiddenQuadruple(HiddenTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 4, 'hidden quadruple')
