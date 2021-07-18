from typing import NamedTuple, List, Set

class Pos(NamedTuple):
    idx: int

    @property
    def x(self) -> int:
        return self.idx % 9

    @property
    def y(self) -> int:
        return self.idx // 9

    @property
    def blk(self) -> int:
        r = self.idx // 27
        c0 = self.idx % 9
        c = c0 // 3
        return r * 3 + c

    def __str__(self):
        return str(self.idx)

    def __eq__(self, idx: int) -> bool:
        return self.idx == idx

    def __ne__(self, idx: int) -> bool:
        return not self.__eq__(idx)

def from_xy(x: int, y: int) -> Pos:
    return Pos(x + y * 9)

class Peer(NamedTuple):
    peer: Set[Pos]

    def __str__(self):
        return f'[{",".join(str(p) for p in sorted(self.peer))}]'

    def __or__(self, p):
        return Peer(self.peer | p.peer)

    def __and__(self, p):
        return Peer(self.peer & p.peer)

    def __contains__(self, n: int) -> bool:
        return n in self.peer

    def __len__(self) -> int:
        return len(self.peer)

def col(n: int) -> Peer:
    return Peer({n * 9 + i for i in range(9)})

def col_from_pos(p: Pos) -> Peer:
    return col(p.y)

def row(n: int) -> Peer:
    return Peer({i * 9 + n for i in range(9)})

def row_from_pos(p: Pos) -> Peer:
    return row(p.x)

def blk(n: int) -> Peer:
    r = n // 3
    c = n % 3
    b = r * 27 + c * 3
    return Peer({b + i for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)})

def blk_from_pos(p: Pos) -> Peer:
    return blk(p.blk)

def peer_from_pos(p: Pos) -> Peer:
    return col_from_pos(p) | row_from_pos(p) | blk_from_pos(p)

class Cell(NamedTuple):
    is_fixed: bool = False
    number: int = 0
    memo: Set[int] = {}

    def __str__(self):
        if self.is_fixed:
            return f'{self.number}'
        else:
            return f'[{"".join([str(n) for n in self.memo])}]'

    def set_number(self, number: int):
        return cell_init(number)

    def remove_memo(self, memo: int):
        m = self.memo.copy()
        return cell_from_memo(m - {memo})

    def remove_memos(self, memos: Set[int]):
        m = self.memo.copy()
        return cell_from_memo(m - memos)

def cell_init(number=0):
    if number > 0:
        return Cell(is_fixed=True, number=number)
    else:
        return Cell(memo=set(range(1,10)))

def cell_from_memo(memo: Set[int]) -> Cell:
    return Cell(memo=memo)


class Sudoku(NamedTuple):
    pos: Pos
    cell: Cell

def set_at(sudoku: List[Sudoku], p: Pos, n: int) -> List[Sudoku]:
    def el(sudoku: Sudoku, p: Pos, n: int) -> Sudoku:
        if sudoku.cell.is_fixed:
            return sudoku
        elif p == sudoku.pos:
            return Sudoku(sudoku.pos, cell_init(n))
        elif sudoku.pos.idx in peer_from_pos(p):
            return Sudoku(sudoku.pos, sudoku.cell.remove_memo(n))
        else:
            return sudoku
    return [el(s, p, n) for s in sudoku]

def sudoku_load(game: str) -> Sudoku:
    from functools import reduce
    def put_at(sudoku: List[Sudoku], cell: (int, str)) -> List[Sudoku]:
        p, c = cell
        if c in '123456789':
            return set_at(sudoku, Pos(p), int(c))
        return sudoku
    sudoku = [Sudoku(Pos(n), cell_init(0)) for n in range(81)]
    problem = [c for c in game if c in '123456789.']

    return reduce(put_at, enumerate(problem), sudoku)

def pprint(sudoku: List[Sudoku]):
    width = max(3, max(len(str(s.cell)) for s in sudoku))
    for y in range(9):
        if y > 0 and y % 3 == 0:
            print('---' * width + '+' + '---' * width + '+' + '---' * width)
        for x in range(9):
            if x > 0 and x % 3 == 0:
                print('|', end='')
            print(f'{str(sudoku[y*9+x].cell):^{width}}', end='')
        print()


class SingleCandidate(NamedTuple):
    pos: Pos
    number: int

    def __str__(self):
        return f'{self.pos.idx}, {self.number}'


def find_single_candidate(sudoku: List[Sudoku]) -> List[SingleCandidate]:
    return [SingleCandidate(s.pos, s.cell.memo.copy().pop())
            for s in sudoku
            if len(s.cell.memo) == 1]


def apply_single_candidates(sudoku: List[Sudoku], candidates: List[SingleCandidate]) -> List[Sudoku]:
    from functools import reduce
    return reduce(lambda s, c: set_at(s, c.pos, c.number), candidates, sudoku)
