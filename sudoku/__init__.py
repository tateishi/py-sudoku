from . import cli
from . import core

#from .model import Sudoku
from .algorithm import (
    NakedTuple, HiddenTuple,
    NakedSingle, HiddenSingle,
    NakedDouble, HiddenDouble,
    NakedTriple, HiddenTriple,
    NakedQuadruple, HiddenQuadruple)
from .solver import BaseSolver, Solver


VERSION = '0.0.1'


main = cli.main
