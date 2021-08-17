from __future__ import annotations

from ..model import Place, Peer, Cell, Grid, Sudoku
from . import SingleCandidate, AlgorithmSingle


class NakedSingle(AlgorithmSingle):
    reason = f'naked single'

    def find(self) -> list[SingleCandidate]:
        return [SingleCandidate(g.place, g.fixable, self.reason)
                for g in self.sudoku
                if g.canfix]


class HiddenSingle(AlgorithmSingle):
    reason = 'hidden single'

    def from_peers(self, peer: Peer, where: str) -> list[SingleCandidate]:
        from collections import defaultdict
        def count_numbers(d: defaultdict, g: Grid) -> defauldict:
            if not g.fixed:
                for m in g.memo:
                    d[m].append(g.i)
            return d

        from functools import reduce
        grids = (self.sudoku[p] for p in peer.peer)
        candidates = reduce(count_numbers, grids, defaultdict(list))
        r = f'{self.reason} {where}'
        return (SingleCandidate(Place(v[0]), k, r)
                for k, v in candidates.items() if len(v) == 1)

    def find(self) -> list[SingleCandidate]:
        from itertools import chain
        return chain.from_iterable(chain(
            (self.from_peers(Peer.col(n), f'col{n}') for n in range(9)),
            (self.from_peers(Peer.row(n), f'row{n}') for n in range(9)),
            (self.from_peers(Peer.blk(n), f'blk{n}') for n in range(9))
        ))
