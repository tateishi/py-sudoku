from __future__ import annotations

from ..model import Place, Peer, Cell, Grid, Sudoku
from . import Algorithm, NakedSingle, HiddenSingle, NakedDouble, HiddenDouble


class BruteForce(Algorithm):
    def trial(self, sudoku: Sudoku) -> Sequence[Sudoku]:
        from functools import reduce

        def choice(sudoku: Sudoku) -> Grid:
            return min((g for g in sudoku if not g.fixed), key=lambda a: a.i)

        def fix(sudoku: Sudoku, grid: Grid, value: int) -> Sudoku:
            return sudoku.fix(grid.place, value)

        def composite(f, g):
            return lambda *args, **kwargs: g(f(*args, **kwargs))

        extra = reduce(composite,
                      [
                       fix,
                       lambda s: NakedSingle(s).solve(),
                       lambda s: HiddenSingle(s).solve(),
                       ])
        grid = choice(sudoku)
        result = (extra(sudoku, grid, v) for v in grid.memo)

        return (sudoku for sudoku in result if not sudoku.fail)


    def step(self, sudokus: list[Sudoku]) -> tuple[bool, list[Sudoku]]:
        result = (self.trial(sudoku) for sudoku in sudokus)

        from itertools import chain
        r = list(chain(*result))
        solved = [s for s in r if s.solved]
        if len(solved) > 0:
            return True, solved
        else:
            return False, r

    def solve(self) -> Sudoku | None:
        flag, s = self.step([self.sudoku])
        while not flag:
            flag, s = self.step(s)
        return s[0]
