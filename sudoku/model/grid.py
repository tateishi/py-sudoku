from __future__ import annotations
from dataclasses import dataclass

from . import Place, Cell


@dataclass
class Grid:
    place: Place
    cell: Cell
