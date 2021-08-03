from __future__ import annotations
from typing import Set
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Cell:
    content: int | set[int] = field(default_factory=set)

    @property
    def fixed(self):
        return isinstance(self.content, int)

    def __str__(self):
        if self.fixed:
            return str(self.content)
        else:
            return f'[{"".join(str(n) for n in sorted(self.content))}]'

    def __sub__(self, n):
        return self.discard(n)

    @classmethod
    def from_number(cls, number: int = 0) -> Cell:
        if number > 0:
            return cls(content=number)
        else:
            return cls(content=set(range(1,10)))

    @classmethod
    def unknown(cls) -> Cell:
        return cls.from_number(0)

    @classmethod
    def from_memo(cls, memo: Set[int]) -> Cell:
        return cls(content=memo)

    def discard(self, memo: int):
        m = self.content.copy()
        m.discard(memo)
        return type(self).from_memo(m)

    # def remove_memos(self, memos: Set[int]):
    #     m = self.memo.copy()
    #     return CellBasic.from_memo(m - memos)


@dataclass
class CellBasic:
    pass
# @dataclass
# class CellBasic:
#     fixed: bool = False
#     number: int = 0
#     memo: Set[int] = field(default_factory=set)

#     def __str__(self):
#         if self.fixed:
#             return f'{self.number}'
#         else:
#             return f'[{"".join([str(n) for n in sorted(self.memo)])}]'

#     def set_number(self, number: int):
#         return CellBasic.from_number(number)

#     def remove_memo(self, memo: int):
#         m = self.memo.copy()
#         return CellBasic.from_memo(m - {memo})

#     def remove_memos(self, memos: Set[int]):
#         m = self.memo.copy()
#         return CellBasic.from_memo(m - memos)

#     @classmethod
#     def from_number(cls, number: int = 0) -> CellBasic:
#         if number > 0:
#             return CellBasic(fixed=True, number=number)
#         else:
#             return CellBasic(memo=set(range(1,10)))

#     @classmethod
#     def unknown(cls) -> CellBasic:
#         return cls.from_number(0)

#     @classmethod
#     def from_memo(cls, memo: Set[int]) -> CellBasic:
#         return CellBasic(memo=memo)
