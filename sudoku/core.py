from __future__ import annotations
from dataclasses import dataclass, field
from functools import reduce
from typing import NamedTuple, List, Set

from . import pos
from . import peer
from . import cellbasic
from . import cell
from . import sudoku

Pos = pos.Pos
Peer = peer.Peer
CellBasic = cellbasic.CellBasic
Cell = cell.Cell
Sudoku = sudoku.Sudoku


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


class Algorithm:
    def __init__(self, sudoku: Sudoku) -> Algorithm:
        self.sudoku = sudoku

    def pprint(self) -> None:
        self.sudoku.pprint()

    def find(self):
        pass

    def apply(self, candidates) -> Sudoku:
        return self.sudoku

    def apply_once(self) -> Sudoku:
        found = self.find()
        return self.apply(found)

    def repeat(self) -> Sudoku:
        self.sudoku.pprint()
        while (o := self.apply_once()) != self.sudoku:
            o.pprint()
            self.sudoku = o
        return o

    def run_once(self) -> None:
        self.sudoku = self.apply_once()

    def run(self) -> None:
        self.sudoku = self.repeat()


class AlgorithmSingle(Algorithm):
    def find(self) -> List[SingleCandidate]:
        return list()

    def apply(self, candidates: List[SingleCandidate]) -> Sudoku:
        from functools import reduce
        return reduce(lambda s, c: Sudoku.set(s, c.pos, c.number),
                      candidates,
                      self.sudoku)

class AlgorithmDouble(Algorithm):
    def find(self) -> List[MultiCandidate]:
        return list()

    def apply(self, candidates: List[MultiCandidate]) -> Sudoku:
        def remove_memo(cell: Cell, p: List[int], memo: Set[int]) -> Cell:
            if cell.pos.idx in p:
                m = cell.cell.memo.copy()
                return Cell(cell.pos, CellBasic.from_memo(m - memo))
            else:
                return cell

        def apply_candidate(s: Sudoku, mc: MultiCandidate) -> Sudoku:
            return Sudoku([remove_memo(c, list(mc.pos), set(mc.number))
                           for c in s])

        from functools import reduce
        return reduce(lambda s, c: apply_candidate(s, c),
                      candidates,
                      self.sudoku)


class NakedSingle(AlgorithmSingle):
    def find(self) -> List[SingleCandidate]:
        return [SingleCandidate(s.pos,
                                s.cell.memo.copy().pop(),
                                f'naked single')
                for s in self.sudoku.cells
                if len(s.cell.memo) == 1]


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


class HiddenSingle(AlgorithmSingle):
    def find_peer(self, peer: Peer, reason: str) -> List[SingleCandidate]:
        def reverse_dict(d: AppendDict, c: Cell) -> AppendDict:
            if not c.cell.fixed:
                for m in c.cell.memo:
                    d[m] = c.pos.idx
            return d

        dict = AppendDict()
        for p in peer.peer:
            dict = reverse_dict(dict, self.sudoku[p])

        r = f'hidden single on {reason}'
        return [SingleCandidate(Pos(v.copy().pop()), k, r)
                for k, v in dict.items() if len(v) == 1]


    def find(self) -> List[SingleCandidate]:
        from operator import add
        from functools import reduce

        candidates = (
            [self.find_peer(Peer.col(n), f'col{n}') for n in range(9)] +
            [self.find_peer(Peer.row(n), f'row{n}') for n in range(9)] +
            [self.find_peer(Peer.blk(n), f'blk{n}') for n in range(9)]
        )

        return reduce(add, candidates)

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
        return s & c.cell.memo


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
