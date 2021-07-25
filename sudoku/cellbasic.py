from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class CellBasic:
    fixed: bool = False
    number: int = 0
    memo: Set[int] = field(default_factory=set)

    def __str__(self):
        if self.fixed:
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
            return CellBasic(fixed=True, number=number)
        else:
            return CellBasic(memo=set(range(1,10)))

    @classmethod
    def unknown(cls) -> CellBasic:
        return cls.from_number(0)

    @classmethod
    def from_memo(cls, memo: Set[int]) -> CellBasic:
        return CellBasic(memo=memo)
