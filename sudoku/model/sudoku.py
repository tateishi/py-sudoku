from __future__ import annotations
from dataclasses import dataclass

from . import Place, Peer, Cell, Grid


@dataclass
class Sudoku:
    grids: list[Grid]

    def __getitem__(self, n):
        return self.grids[n]

    @classmethod
    def load(cls, game: str) -> Sudoku:
        def put_number(sudoku: Sudoku, cell: tuple[int, str]) -> Sudoku:
            p, c = cell
            if c not in '123456789':
                return sudoku
            return sudoku.fix(Place(p), int(c))

        from functools import reduce

        sudoku = Sudoku(Grid.unknown(n) for n in range(81))
        problem = (c for c in game if c in '123456789.')

        return reduce(put_number, enumerate(problem), sudoku)

    def fix(self, p: Place, n: int) -> Sudoku:
        def fix_number(grid: Grid, p: Place, n: int) -> Grid:
            if grid.fixed:
                return grid
            elif p == grid.place:
                return grid.from_number(n)
            elif grid in Peer.peers(p):
                return grid - n
            else:
                return grid
        return Sudoku([fix_number(g, p, n) for g in self.grids])

    def pprint_str(self) -> str:
        import io
        from contextlib import redirect_stdout

        def pp():
            width = max(3, max(len(str(s.cell)) for s in self.grids))
            for y in range(9):
                if y > 0 and y % 3 == 0:
                    print('+'.join(['---' * width] * 3))
                for x in range(9):
                    if x > 0 and x % 3 == 0:
                        print('|', end='')
                    print(f'{str(self.grids[y*9+x].cell):^{width}}', end='')
                print()

        with io.StringIO() as out:
            with redirect_stdout(out):
                pp()

            return out.getvalue()

    def pprint(self) -> None:
        print(self.pprint_str())
