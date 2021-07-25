from . import cli
from . import core

from .game import Sudoku
from .algorithm import (
    NakedTuple, HiddenTuple,
    NakedSingle, HiddenSingle,
    NakedDouble, HiddenDouble,
    NakedTriple, HiddenTriple,
    NakedQuadruple, HiddenQuadruple)

VERSION = '0.0.1'


main = cli.main
