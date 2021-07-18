from functools import reduce
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

class CellBasic(NamedTuple):
    is_fixed: bool = False
    number: int = 0
    memo: Set[int] = set()

    def __str__(self):
        if self.is_fixed:
            return f'{self.number}'
        else:
            return f'[{"".join([str(n) for n in sorted(self.memo)])}]'

    def set_number(self, number: int):
        return cell_basic_init(number)

    def remove_memo(self, memo: int):
        m = self.memo.copy()
        return cell_basic_from_memo(m - {memo})

    def remove_memos(self, memos: Set[int]):
        m = self.memo.copy()
        return cell_basic_from_memo(m - memos)

def cell_basic_init(number=0):
    if number > 0:
        return CellBasic(is_fixed=True, number=number)
    else:
        return CellBasic(memo=set(range(1,10)))

def cell_basic_from_memo(memo: Set[int]) -> CellBasic:
    return CellBasic(memo=memo)


class Cell(NamedTuple):
    pos: Pos
    cell: CellBasic


class Sudoku(NamedTuple):
    cells: List[Cell]


def set_at(sudoku: Sudoku, p: Pos, n: int) -> Sudoku:
    def el(cell: Cell, p: Pos, n: int) -> Cell:
        if cell.cell.is_fixed:
            return cell
        elif p == cell.pos:
            return Cell(cell.pos, cell_basic_init(n))
        elif cell.pos.idx in peer_from_pos(p):
            return Cell(cell.pos, cell.cell.remove_memo(n))
        else:
            return cell
    return Sudoku([el(s, p, n) for s in sudoku.cells])


def sudoku_load(game: str) -> Sudoku:
    from functools import reduce
    def put_at(sudoku: Sudoku, cell: (int, str)) -> Sudoku:
        p, c = cell
        if c in '123456789':
            return set_at(sudoku, Pos(p), int(c))
        return sudoku
    sudoku = Sudoku([Cell(Pos(n), cell_basic_init(0)) for n in range(81)])
    problem = [c for c in game if c in '123456789.']

    return reduce(put_at, enumerate(problem), sudoku)

def pprint(sudoku: Sudoku):
    width = max(3, max(len(str(s.cell)) for s in sudoku.cells))
    for y in range(9):
        if y > 0 and y % 3 == 0:
            print('---' * width + '+' + '---' * width + '+' + '---' * width)
        for x in range(9):
            if x > 0 and x % 3 == 0:
                print('|', end='')
            print(f'{str(sudoku.cells[y*9+x].cell):^{width}}', end='')
        print()


def repeat_until_stable(func, obj):
    while (o := func(obj)) != obj:
        obj = o
    return obj


class SingleCandidate(NamedTuple):
    pos: Pos
    number: int
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.pos.idx}, {self.number}'


def find_single_candidate(sudoku: Sudoku) -> List[SingleCandidate]:
    return [SingleCandidate(s.pos, s.cell.memo.copy().pop(), f'naked single')
            for s in sudoku.cells
            if len(s.cell.memo) == 1]


def apply_single_candidates(sudoku: Sudoku, candidates: List[SingleCandidate]) -> Sudoku:
    from functools import reduce
    return reduce(lambda s, c: set_at(s, c.pos, c.number), candidates, sudoku)


def exec_naked_single(sudoku: Sudoku) -> Sudoku:
    candidates = find_single_candidate(sudoku)
    return apply_single_candidates(sudoku, candidates)


class AppendDict:
    def __init__(self):
        self.dict = dict()

    def append(self, key, value):
        if key in self.dict:
            self.dict[key].append(value)
        else:
            self.dict[key] = [value]

    def items(self):
        return self.dict.items()

    def __getitem__(self, key):
        if key in self.dict:
            return self.dict[key]
        else:
            return set()

    def __setitem__(self, key, value):
        if key in self.dict:
            self.dict[key].add(value)
        else:
            self.dict[key] = set((value,))

    def __str__(self):
        return str(self.dict)

def find_hidden_single_candidates_peer(sudoku: Sudoku, peer: Peer, reason: str) -> List[SingleCandidate]:
    def reverse_dict(d: AppendDict, c: Cell) -> AppendDict:
        if not c.cell.is_fixed:
            for m in c.cell.memo:
                d[m] = c.pos.idx
        return d

    dict = AppendDict()
    for p in peer.peer:
        dict = reverse_dict(dict, sudoku.cells[p])

    return [SingleCandidate(Pos(v.copy().pop()), k, reason) for k, v in dict.items() if len(v) == 1]

def find_hidden_single_candidates(sudoku: Sudoku) -> List[SingleCandidate]:
    from operator import add
    from functools import reduce

    candidates = (
        [find_hidden_single_candidates_peer(sudoku, col(n), f'hidden single on col{n}') for n in range(9)] +
        [find_hidden_single_candidates_peer(sudoku, row(n), f'hidden single on row{n}') for n in range(9)] +
        [find_hidden_single_candidates_peer(sudoku, blk(n), f'hidden single on blk{n}') for n in range(9)]
    )

    return reduce(add, candidates)

def exec_hidden_single(sudoku: Sudoku) -> Sudoku:
    candidates = find_hidden_single_candidates(sudoku)
    return apply_single_candidates(sudoku, candidates)
