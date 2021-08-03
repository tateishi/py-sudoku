from __future__ import annotations
from typing import List

from ..model import Pos, Peer, Cell, Sudoku
from . import SingleCandidate, AlgorithmSingle, AppendDict


class NakedSingle(AlgorithmSingle):
    def find(self) -> List[SingleCandidate]:
        return [SingleCandidate(s.pos,
                                s.cell.memo.copy().pop(),
                                f'naked single')
                for s in self.sudoku.cells
                if len(s.cell.memo) == 1]


class HiddenSingle(AlgorithmSingle):
    def find_peer(self, peer: Peer, reason: str) -> List[SingleCandidate]:
        def reverse_dict(d: AppendDict, c: Cell) -> AppendDict:
            if not c.cell.fixed:
                for m in c.cell.memo:
                    d[m] = c.pos.idx
            return d

        dict = AppendDict()
        for p in peer.peer:
            dict = reverse_dict(dict, self.sudoku.cells[p])

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
