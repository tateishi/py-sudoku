from __future__ import annotations

from ..model import Place, Peer, Cell, Grid, Sudoku
from . import SingleCandidate, MultiCandidate


class Algorithm:
    reason = ''

    def __init__(self, sudoku: Sudoku) -> None:
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

    def solve(self) -> Sudoku:
        return self.repeat()

class AlgorithmSingle(Algorithm):
    def find(self) -> list[SingleCandidate]:
        return list()

    def apply(self, candidates: list[SingleCandidate]) -> Sudoku:
        def fix(s: Sudoku, c: SingleCandidate) -> Sudoku:
            return s.fix(c.place, c.number)

        from functools import reduce
        return reduce(fix, candidates, self.sudoku)

class AlgorithmDouble(Algorithm):
    def find(self) -> list[MultiCandidate]:
        return list()

    def apply(self, candidates: list[MultiCandidate]) -> Sudoku:
        return self.sudoku
