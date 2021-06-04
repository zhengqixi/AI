from solver import Solver, SolveType
from parser import Parser


class CMD:
    def __init__(self, input_file: str, solver_type: str,
                 prune: bool, verbose: bool) -> None:
        self._solver_type = solver_type
        self._prune = prune
        self._verbose = verbose
        self._input_file = input_file
        self._parser = Parser()
        self._solver = Solver()
        if solver_type == 'min':
            self._solver_type = SolveType.MIN
        elif solver_type == 'max':
            self._solver_type = SolveType.MAX
        else:
            raise Exception('invalid type')

    def execute(self):
        root = self._parser.generate_from_file(self._input_file)
        self._solver.solve(root, self._solver_type, self._prune, self._verbose)

CMD('test1.test', 'max', False, True).execute()
