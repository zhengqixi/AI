from node import Node
from enum import Enum
from typing import List, Tuple


class SolveType(Enum):
    MAX = 0
    MIN = 1


class Solver:

    def solve(self, start: Node, start_type: 'SolveType',
              prune: bool = False, verbose: bool = False) -> None:
        if prune == True:
            self._alpha_beta(start, start_type, verbose)
        else:
            self._minimax(start, start_type, verbose)

    def _minimax(self, start: Node, start_type: 'SolveType',
                 verbose: bool) -> Tuple[Node, int]:
        # If we're a leaf node...not much choice here
        if start.is_leaf:
            return [start, start.value]
        next_level_type = self._switch_type(start_type)
        traverse_results = [
            self._minimax(
                x,
                next_level_type,
                verbose) for x in start.children]
        should_choose = self._selector(traverse_results, start_type)
        if verbose == True:
            self._print(start, should_choose[0], should_choose[1], start_type)
        return [start, should_choose[1]]

    def _selector(self, nodes: List[Tuple[Node, int]],
                  select_type: 'SolveType') -> Tuple[Node, int]:
        if select_type == SolveType.MAX:
            return max(nodes, key=lambda k: k[1])
        else:
            return min(nodes, key=lambda k: k[1])

    def _alpha_beta(self, start: Node, start_type: 'SolveType',
                    verbose: bool) -> Tuple[Node, int]:
        raise NotImplementedError("oh nodes")

    def _switch_type(self, select_type: 'SolveType') -> 'SolveType':
        if select_type == SolveType.MAX:
            return SolveType.MIN
        return SolveType.MAX
    
    def _print(self, start_node: Node, choice: Node, value: int, select_type: 'SolveType') -> None:
        chooses_str = 'chooses {} for {}'.format(choice.label, value)
        if select_type == SolveType.MIN:
            print('min({}) {}'.format(start_node.label, chooses_str))
        else:
            print('max({}) {}'.format(start_node.label, chooses_str))
