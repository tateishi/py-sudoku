from __future__ import annotations
from collections.abc import Sequence

from ..model import Place, Cell, Grid, Peer, Sudoku
from . import MultiCandidate, AlgorithmDouble


class AlgorithmTuple(AlgorithmDouble):
    def __init__(self, sudoku: Sudoku, n: int):
        self.n = n
        super().__init__(sudoku)

    def inclusive(self, g: Grid, s: set[int]) -> bool:
        return True

    def candidate_peer(self, p: list[int], v: list[int]) -> list[int]:
        return list()

    def from_peers(self, peer: Peer, where: str) -> Sequence[MultiCandidate]:
        from operator import or_
        from functools import reduce
        from itertools import combinations, product
        from collections import defaultdict

        def choicedict(d: defaultdict, x: tuple(Grid, set[int])) -> defaultdict:
            g, s = x
            if self.inclusive(g, s):
                d[frozenset(s)].append(g.i)
            return d

        def get_candidates(numbers: defaultdict, grids: Sequence[Grid], where: str) -> Sequence[MultiCandidate]:
            p = [g.i for g in grids]
            r = f'{self.reason} on {where}'
            return (MultiCandidate(self.candidate_peer(p, v), list(k), r)
                    for k, v in numbers.items()
                    if len(v) == self.n)

        grids = [g for g in self.sudoku[peer] if not g.fixed]
        if len(grids) == 0: return list()

        nums = reduce(or_, (g.cell.content for g in grids))
        combi = (set(s) for s in combinations(nums, self.n))

        numbers = reduce(choicedict, product(grids, combi), defaultdict(list))

        return get_candidates(numbers, grids, where)

    def find(self) -> Sequence[MultiCandidate]:
        from itertools import chain
        return chain.from_iterable(chain(
            (self.from_peers(Peer.col(n), f'col{n}') for n in range(9)),
            (self.from_peers(Peer.row(n), f'row{n}') for n in range(9)),
            (self.from_peers(Peer.blk(n), f'blk{n}') for n in range(9))
        ))

    def new_grid(self, grid: Grid, memo: Sequence[int]) -> Grid:
        return Grid()

    def apply(self, candidates: Sequence[MultiCandidate]) -> Sudoku:
        def remove(grid: Grid, p: list[Place], memo: Sequence[int]) -> Grid:
            if grid.i in p:
                return self.new_grid(grid, memo)
            return grid

        def apply_(s: Sudoku, mc: MultiCandidate) -> Sudoku:
            return Sudoku([remove(grid, mc.places, mc.number) for grid in s])

        from functools import reduce
        return reduce(apply_, candidates, self.sudoku)


class NakedTuple(AlgorithmTuple):
    def inclusive(self, g: Grid, s: set[int]) -> bool:
        return s >= g.cell.content

    def candidate_peer(self, p: list[int], v: list[int]) -> list[int]:
        return list(set(p) - set(v))

    def new_grid(self, grid: Grid, memo: Sequence[int]) -> Grid:
        return grid.from_memo(grid.cell.content - set(memo))


class HiddenTuple(AlgorithmTuple):
    def inclusive(self, g: Grid, s: set[int]) -> bool:
        return bool(s & g.cell.content)

    def candidate_peer(self, p: list[int], v: list[int]) -> list[int]:
        return v

    def new_grid(self, grid: Grid, memo: Sequence[int]) -> Grid:
        return grid.from_memo(grid.cell.content & set(memo))


class NakedDouble(NakedTuple):
    reason = 'Naked Double'

    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 2)


class HiddenDouble(HiddenTuple):
    reason = 'Hidden Double'

    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 2)


class NakedTriple(NakedTuple):
    reason = 'Naked Triple'

    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 3)


class HiddenTriple(HiddenTuple):
    reason = 'Hidden Triple'

    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 3)


class NakedQuadruple(NakedTuple):
    reason = 'Naked Quadruple'

    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 4)


class HiddenQuadruple(HiddenTuple):
    reason = 'Hidden Quadruple'

    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 4)
