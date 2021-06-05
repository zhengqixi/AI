from node import Node
from enum import Enum
from typing import List, Tuple
from math import inf
from queue import Queue


class SolveType(Enum):
    MAX = 0
    MIN = 1


class SolveStep:
    def __init__(self, parent: Node, selected: Node,
                 select_type: 'SolveType', value: int) -> None:
        self._parent = parent
        self._selected = selected
        self._select_type = select_type
        self._value = value

    @property
    def parent(self) -> Node:
        return self._parent

    @property
    def selected(self) -> Node:
        return self._selected

    @property
    def select_type(self) -> 'SolveType':
        return self._select_type

    @property
    def value(self) -> int:
        return self._value


class Solver:

    """
    Solver contains the logic that performs minimax and alpha-beta minimax search
    NOTE:
    Both minimax and alphabeta recursion step functions return a tuple of [Node, int]
    The node returned is also the same as the node passed in
    Arguably, I don't need to do it this way,
    but IMO it works out cleaner this way
    """

    def solve(self, start: Node, start_type: 'SolveType',
              prune: bool = False) -> 'Queue[SolveStep]':
        """
        Solves the provided DAG using minimax
        """
        if prune == True:
            return self._alpha_beta(start, start_type)
        else:
            return self._minimax(start, start_type)

    def _minimax(self, start: Node,
                 start_type: 'SolveType') -> 'Queue[SolveStep]':
        """
        Header recurse function for minimax
        """
        queue = Queue()
        self._minimax_step(start, start_type, queue)
        return queue

    def _minimax_step(self, start: Node, start_type: 'SolveType',
                      steps: 'Queue[SolveStep]') -> Tuple[Node, int]:
        """
        Recurses into nodes and their children
        """
        if start.is_leaf:
            return [start, start.value]
        next_level_type = self._switch_type(start_type)
        traverse_results = [self._minimax_step(
            x, next_level_type, steps) for x in start.children]
        should_choose = self._selector(traverse_results, start_type)
        step = SolveStep(start, should_choose[0], start_type, should_choose[1])
        steps.put(step)
        return [start, should_choose[1]]

    def _selector(self, nodes: List[Tuple[Node, int]],
                  select_type: 'SolveType') -> Tuple[Node, int]:
        """
        Helper function to select best node among children
        """
        if select_type == SolveType.MAX:
            return max(nodes, key=lambda k: k[1])
        else:
            return min(nodes, key=lambda k: k[1])

    def _alpha_beta(self, start: Node,
                    start_type: 'SolveType') -> 'Queue[SolveStep]':
        """
        Header recurse function for alpha-beta pruned minimax
        """
        queue = Queue()
        self._alpha_beta_step(start, start_type, -inf, inf, queue)
        return queue

    def _alpha_beta_step(self, start: Node, start_type: 'SolveType',
                         alpha: int, beta: int, steps: 'Queue[SolveStep]') -> Tuple[Node, int]:
        """
        Recurse step for alpha beta pruning
        With some clever functional programming, this code can probably be DRY'd up
        But it would be a bit more confusing to read, and its not worth the effort
        for a school assignment
        """
        if start.is_leaf:
            return [start, start.value]
        next_level_type = self._switch_type(start_type)
        if start_type == SolveType.MAX:
            chosen_set = [None, -inf]
            for child in start.children:
                chosen = self._alpha_beta_step(
                    child, next_level_type, alpha, beta, steps)
                if chosen is None:
                    continue
                chosen_set = max(chosen, chosen_set, key=lambda k: k[1])
                if chosen_set[1] >= beta:
                    return None
                alpha = chosen_set[1]
            step = SolveStep(start, chosen_set[0], start_type, chosen_set[1])
            steps.put(step)
            return [start, chosen_set[1]]
        else:
            chosen_set = [None, inf]
            for child in start.children:
                chosen = self._alpha_beta_step(
                    child, next_level_type, alpha, beta, steps)
                if chosen is None:
                    continue
                chosen_set = min(chosen, chosen_set, key=lambda k: k[1])
                if chosen_set[1] <= alpha:
                    return None
                beta = chosen_set[1]
            step = SolveStep(start, chosen_set[0], start_type, chosen_set[1])
            steps.put(step)
            return [start, chosen_set[1]]

    def _switch_type(self, select_type: 'SolveType') -> 'SolveType':
        """
        Utility to I don't have to write this if over and over
        """
        if select_type == SolveType.MAX:
            return SolveType.MIN
        return SolveType.MAX
