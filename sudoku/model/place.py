from __future__ import annotations
from dataclasses import dataclass


@dataclass(order=True, frozen=True)
class Place:
    index: int

    def __str__(self):
        return str(self.index)

    def __format__(self, fmt):
        import re
        if fmt[-1] == 'n':
            sep = ''
            fmt = fmt[:-1]
        else:
            sep = ','
        types = 'ixyb'
        fields = { c : getattr(self, c) for c in types }
        comp = re.compile(f'([^{types}]*)([{types}]*)$')
        match = comp.match(fmt)
        if match:
            fmt, types_m = match.group(1, 2)
            types_m = types_m or types[0]
            result = (f'{fields[p]:{fmt}}' for p in types if p in types_m)
            return sep.join(result)
        else:
            raise ValueError(f"Unknown format code '{fmt}'")

    def __int__(self) -> int:
        return self.index

    @classmethod
    def from_xy(cls, x: int, y: int) -> cls:
        return cls(x + y * 9)

    @property
    def i(self) -> int:
        return self.index

    @property
    def xy(self) -> (int, int):
        y, x = divmod(self.index, 9)
        return x, y

    @property
    def x(self) -> int:
        return self.xy[0]

    @property
    def y(self) -> int:
        return self.xy[1]

    @property
    def b(self) -> int:
        x, y = self.xy
        r = y // 3
        c = x // 3
        return r * 3 + c
