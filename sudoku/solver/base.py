from ..model import Sudoku
from ..algorithm import NakedSingle, HiddenSingle, NakedDouble, HiddenDouble, NakedTriple, HiddenTriple, NakedQuadruple, HiddenQuadruple

class BaseSolver:
    def __init__(self, algorithms=None, sudoku=None):
        self.algorithms = algorithms
        self.sudoku = sudoku
        self.result = None

    def load(self, s:str) -> None:
        self.sudoku = Sudoku.load(s)

    def run_once(self, algorithm):
        print(f'run_once: {algorithm}')
        algo = algorithm(self.sudoku)
        algo.run()
        return algo.sudoku

    def run_loop(self, algorithms):
        old = self.sudoku
        print(f'run_loop: {algorithms}')
        for algo in algorithms:
            new = self.run_once(algo)
            if old != new:
                return new
        return old

    def run(self):
        print(f'run: {self.algorithms}')
        while True:
            new = self.run_loop(self.algorithms)
            if self.sudoku == new:
                self.result = self.sudoku
                return
            self.sudoku = new


class Solver(BaseSolver):
    algorithms = [
        NakedSingle,
        HiddenSingle,
        NakedDouble,
        HiddenDouble,
        NakedTriple,
        HiddenTriple,
        NakedQuadruple,
        HiddenQuadruple,
    ]

    def __init__(self, sudoku: Sudoku=None) -> None:
        super().__init__(self.algorithms, sudoku)

    def pprint(self) -> None:
        self.sudoku.pprint()
