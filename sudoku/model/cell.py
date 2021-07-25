from __future__ import annotations
from dataclasses import dataclass

from . import Pos, CellBasic


@dataclass
class Cell:
    pos: Pos
    cell: CellBasic
