from __future__ import annotations
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


# @dataclass
# class Cell:
#     pos: Pos
#     cell: CellBasic
