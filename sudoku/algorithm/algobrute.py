from __future__ import annotations

from ..model import Place, Peer, Cell, Grid, Sudoku
from . import Algorithm


class BruteForce(Algorithm):
    def choice(self, sudoku: Sudoku) -> Grid:
        return min((g for g in sudoku if not g.fixed), key=lambda a: a.i)

    def fix(self, sudoku: Sudoku, grid: Grid, value: int) -> Sudoku:
        return sudoku.fix(grid.place, value)

    def trial(self, sudoku: Sudoku) -> list[Sudoku]:
        grid = self.choice(sudoku)
        return [self.fix(sudoku, grid, v) for v in grid.memo]
