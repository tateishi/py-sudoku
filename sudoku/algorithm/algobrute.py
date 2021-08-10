from __future__ import annotations

from ..model import Place, Peer, Cell, Grid, Sudoku
from . import Algorithm, NakedSingle, HiddenSingle, NakedDouble, HiddenDouble


class BruteForce(Algorithm):
    def choice(self, sudoku: Sudoku) -> Grid:
        return min((g for g in sudoku if not g.fixed), key=lambda a: a.i)

    def nakedsingle(self, sudoku: Sudoku) -> Sudoku:
        algo = NakedSingle(sudoku)
        return algo.repeat()

    def hiddensingle(self, sudoku: Sudoku) -> Sudoku:
        algo = HiddenSingle(sudoku)
        return algo.repeat()

    def nakeddouble(self, sudoku: Sudoku) -> Sudoku:
        algo = NakedDouble(sudoku)
        return algo.repeat()

    def hiddendouble(self, sudoku: Sudoku) -> Sudoku:
        algo = HiddenDouble(sudoku)
        return algo.repeat()

    def fix(self, sudoku: Sudoku, grid: Grid, value: int) -> Sudoku:
        return sudoku.fix(grid.place, value)

    def trial(self, sudoku: Sudoku) -> list[Sudoku]:
        grid = self.choice(sudoku)
        result = (self.fix(sudoku, grid, v) for v in grid.memo)
        result = (self.nakedsingle(sudoku) for sudoku in result)
        result = (self.hiddensingle(sudoku) for sudoku in result)
        return [sudoku for sudoku in result if not sudoku.fail]

    def step(self, sudokus: list[Sudoku]) -> tuple[bool, list[Sudoku]]:
        result = [self.trial(sudoku) for sudoku in sudokus]
        from operator import add
        from functools import reduce
        r = reduce(add, result)
        solved = [s for s in r if s.solved]
        if len(solved) > 0:
            return True, solved
        else:
            return False, r

    def solve(self, sudoku: Sudoku) -> Sudoku | None:
        flag, s = self.step([sudoku])
        while not flag:
            print(len(s))
            flag, s = self.step(s)
        return s[0]
