from ..model import Sudoku


class BaseSolver:
    def __init__(self, sudoku, algorithms):
        self.sudoku = sudoku
        self.algorithms = algorithms
        self.result = None

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
    pass
