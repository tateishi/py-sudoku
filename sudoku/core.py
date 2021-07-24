from __future__ import annotations
from dataclasses import dataclass, field
from functools import reduce
from typing import NamedTuple, List, Set


@dataclass
class Pos:
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

    @classmethod
    def from_xy(cls, x: int, y: int) -> Pos:
        return Pos(x + y * 9)


@dataclass
class Peer:
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

    @classmethod
    def col(cls, p) -> Peer:
        if isinstance(p, int):
            return Peer({i * 9 + p for i in range(9)})
        elif isinstance(p, Pos):
            return Peer.col(p.x)
        else:
            raise TypeError

    @classmethod
    def row(cls, p) -> Peer:
        if isinstance(p, int):
            return Peer({p * 9 + i for i in range(9)})
        elif isinstance(p, Pos):
            return Peer.row(p.y)
        else:
            raise TypeError

    @classmethod
    def blk(cls, p) -> Peer:
        if isinstance(p, int):
            r = p // 3
            c = p % 3
            b = r * 27 + c * 3
            return Peer({b + i for i in (0, 1, 2, 9, 10, 11, 18, 19, 20)})
        elif isinstance(p, Pos):
            return Peer.blk(p.blk)
        else:
            raise TypeError

    @classmethod
    def peers(cls ,p: Pos) -> Peer:
        return Peer.col(p) | Peer.row(p) | Peer.blk(p)


@dataclass
class CellBasic:
    is_fixed: bool = False
    number: int = 0
    memo: Set[int] = field(default_factory=set)

    def __str__(self):
        if self.is_fixed:
            return f'{self.number}'
        else:
            return f'[{"".join([str(n) for n in sorted(self.memo)])}]'

    def set_number(self, number: int):
        return CellBasic.from_number(number)

    def remove_memo(self, memo: int):
        m = self.memo.copy()
        return CellBasic.from_memo(m - {memo})

    def remove_memos(self, memos: Set[int]):
        m = self.memo.copy()
        return CellBasic.from_memo(m - memos)

    @classmethod
    def from_number(cls, number: int = 0) -> CellBasic:
        if number > 0:
            return CellBasic(is_fixed=True, number=number)
        else:
            return CellBasic(memo=set(range(1,10)))

    @classmethod
    def unknown(cls) -> CellBasic:
        return cls.from_number(0)

    @classmethod
    def from_memo(cls, memo: Set[int]) -> CellBasic:
        return CellBasic(memo=memo)


@dataclass
class Cell:
    pos: Pos
    cell: CellBasic


@dataclass
class Sudoku:
    cells: List[Cell]

    def __getitem__(self, idx):
        return self.cells[idx]

    @classmethod
    def load(cls, game: str) -> Sudoku:
        from functools import reduce

        def put_at(sudoku: Sudoku, cell: (int, str)) -> Sudoku:
            p, c = cell
            if c in '123456789':
                return cls.set(sudoku, Pos(p), int(c))
            return sudoku

        sudoku = Sudoku(Cell(Pos(n), CellBasic.unknown()) for n in range(81))
        problem = [c for c in game if c in '123456789.']

        return reduce(put_at, enumerate(problem), sudoku)

    @classmethod
    def set(cls, s: Sudoku, p: Pos, n: int) -> Sudoku:
        def el(cell: Cell, p: Pos, n: int) -> Cell:
            if cell.cell.is_fixed:
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


@dataclass
class SingleCandidate:
    pos: Pos
    number: int
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.pos.idx}, {self.number}'


@dataclass
class MultiCandidate:
    pos: List[int]
    number: List[int]
    reason: str = 'unkown'

    def __str__(self):
        return f'{self.pos}, {self.number}'


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
        self.sudoku.pprint()
        while (o := self.apply_once()) != self.sudoku:
            o.pprint()
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


class NakedSingle(AlgorithmSingle):
    def find(self) -> List[SingleCandidate]:
        return [SingleCandidate(s.pos,
                                s.cell.memo.copy().pop(),
                                f'naked single')
                for s in self.sudoku.cells
                if len(s.cell.memo) == 1]


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


class HiddenSingle(AlgorithmSingle):
    def find_peer(self, peer: Peer, reason: str) -> List[SingleCandidate]:
        def reverse_dict(d: AppendDict, c: Cell) -> AppendDict:
            if not c.cell.is_fixed:
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

class AlgorithmTuple(AlgorithmDouble):
    def __init__(self, sudoku: Sudoku, n: int, name: str):
        self.n = n
        self.name = name
        super().__init__(sudoku)

    def inclusive(self, c: Cell, s: set[int]) -> bool:
        return True

    def find_peer(self, peer: Peer, reason: str) -> List[MultiCandidate]:
        def reverse_dict(d: AppendDict, c: Cell, s: set[int]) -> AppendDict:
            if self.inclusive(c, s):
                d[frozenset(s)] = c.pos.idx
            return d


        from operator import or_
        from functools import reduce
        from itertools import combinations

        peers = [self.sudoku.cells[p] for p in peer.peer
                 if not self.sudoku.cells[p].cell.is_fixed]
        if len(peers) == 0: return list()
        memos = reduce(or_, (c.cell.memo for c in peers))
        sets = [set(s) for s in combinations(memos, self.n)]

        dict = AppendDict()
        for s in sets:
            for p in peers:
                dict = reverse_dict(dict, p, s)

        p0 = {p.pos.idx for p in peers}
        r = f'{self.name} on {reason}'
        candidates = [MultiCandidate(list(p0-v), list(k), r)
                      for k, v in dict.dict.items()
                      if len(v) == self.n]
        return candidates

    def find(self) -> List[MultiCandidate]:
        from operator import add
        from functools import reduce

        candidates = (
            [self.find_peer(Peer.col(n), f'col{n}') for n in range(9)] +
            [self.find_peer(Peer.row(n), f'row{n}') for n in range(9)] +
            [self.find_peer(Peer.blk(n), f'blk{n}') for n in range(9)]
        )

        return reduce(add, candidates)


class NakedTuple(AlgorithmTuple):
    def inclusive(self, c: Cell, s: set[int]) -> bool:
        return s >= c.cell.memo


class HiddenTuple(AlgorithmTuple):
    def inclusive(self, c: Cell, s: set[int]) -> bool:
        return s & c.cell.memo


class NakedDouble(NakedTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 2, 'naked double')


class HiddenDouble(HiddenTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 2, 'hidden double')


class NakedTriple(NakedTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 3, 'naked triple')


class HiddenTriple(HiddenTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 3, 'hidden triple')


class NakedQuadruple(NakedTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 4, 'naked quadruple')


class HiddenQuadruple(HiddenTuple):
    def __init__(self, sudoku: Sudoku):
        super().__init__(sudoku, 4, 'hidden quadruple')
