from __future__ import annotations
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Cell:
    content: int | set[int]

    @property
    def fixed(self):
        return isinstance(self.content, int)

    def __str__(self):
        if self.fixed:
            return str(self.content)
        else:
            return f'[{"".join(str(n) for n in sorted(self.content))}]'

    def __sub__(self, n: int | Sequence[int]) -> Cell:
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
    def from_memo(cls, memo: Sequence[int]) -> Cell:
        if isinstance(memo, set):
            return cls(content=memo)
        elif isinstance(memo, Sequence):
            return cls(content=set(memo))
        else:
            raise NotImplementedError

    def discard(self, memo: int | Sequence[int]) -> Cell:
        if isinstance(self.content, int):
            return self

        m = self.content.copy()
        if isinstance(memo, int):
            m.discard(memo)
        elif isinstance(memo, set):
            m = m - memo
        elif isinstance(memo, Sequence):
            m = m - set(memo)
        else:
            raise NotImplementedError
        return type(self).from_memo(m)
