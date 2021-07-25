from __future__ import annotations
from dataclasses import dataclass, field
from functools import reduce

from ..game import Pos, Peer, CellBasic, Cell, Sudoku
from . import SingleCandidate, MultiCandidate


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
        while (o := self.apply_once()) != self.sudoku:
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
