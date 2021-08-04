from __future__ import annotations
from typing import List, Tuple
from dataclasses import dataclass

#from . import Pos, Peer, CellBasic, Cell


@dataclass
class Sudoku:
    cells: List[Cell]

    def __getitem__(self, idx):
        return self.cells[idx]

    @classmethod
    def load(cls, game: str) -> Sudoku:
        from functools import reduce

        def put_at(sudoku: Sudoku, cell: Tuple[int, str]) -> Sudoku:
            p, c = cell
            if c in '123456789':
                return cls.set(sudoku, Pos(p), int(c))
            return sudoku

        sudoku = Sudoku([Cell(Pos(n), CellBasic.unknown()) for n in range(81)])
        problem = [c for c in game if c in '123456789.']

        return reduce(put_at, enumerate(problem), sudoku)

    @classmethod
    def set(cls, s: Sudoku, p: Pos, n: int) -> Sudoku:
        def el(cell: Cell, p: Pos, n: int) -> Cell:
            if cell.cell.fixed:
                return cell
            elif p == cell.pos:
                return Cell(cell.pos, CellBasic.from_number(n))
            elif cell.pos.idx in Peer.peers(p):
                return Cell(cell.pos, cell.cell.remove_memo(n))
            else:
                return cell
        return Sudoku([el(s, p, n) for s in s.cells])

    def pprint_str(self) -> str:
        import io
        from contextlib import redirect_stdout

        def pp():
            width = max(3, max(len(str(s.cell)) for s in self.cells))
            for y in range(9):
                if y > 0 and y % 3 == 0:
                    print('+'.join(['---' * width] * 3))
                for x in range(9):
                    if x > 0 and x % 3 == 0:
                        print('|', end='')
                    print(f'{str(self.cells[y*9+x].cell):^{width}}', end='')
                print()

        with io.StringIO() as out:
            with redirect_stdout(out):
                pp()

            return out.getvalue()

    def pprint(self) -> None:
        print(self.pprint_str())
