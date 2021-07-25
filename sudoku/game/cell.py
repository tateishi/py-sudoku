from __future__ import annotations
from dataclasses import dataclass

from .pos import Pos
from .cellbasic import CellBasic


@dataclass
class Cell:
    pos: Pos
    cell: CellBasic
