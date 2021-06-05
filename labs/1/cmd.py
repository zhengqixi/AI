from solver import Solver, SolveType, SolveStep
from parser import Parser
from queue import Queue


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
        """
        Execute minimax search on graph
        """
        root = self._parser.generate_from_file(self._input_file)
        steps = self._solver.solve(
            root, self._solver_type, self._prune)
        self._print(steps, self._verbose)

    def _print(self, steps: 'Queue[SolveStep]', verbose: bool) -> None:
        """
        Print the entire output from traversal
        """
        if verbose:
            while steps.empty() == False:
                self._print_step(steps.get())
        else:
            last_step = None
            while steps.empty() == False:
                last_step = steps.get()
            self._print_step(last_step)

    def _print_step(self, step: SolveStep) -> None:
        """
        Print a single traversal step
        """
        chooses_str = 'chooses {} for {}'.format(
            step.selected.label, step.value)
        if step.select_type == SolveType.MIN:
            print('min({}) {}'.format(step.parent.label, chooses_str))
        else:
            print('max({}) {}'.format(step.parent.label, chooses_str))
