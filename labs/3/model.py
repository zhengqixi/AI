from typing import Dict, List, Tuple
import numpy.typing as npt

import numpy as np


class ParseException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Node:

    def __init__(self, name: str) -> None:
        self._name = name
        self._reward = 0
        self._edges = []
        self._transition_probabilities = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def reward(self) -> float:
        return self._reward

    @reward.setter
    def reward(self, reward: float) -> None:
        self._reward = reward

    def calculate_transition_probabilities(self, policy: Dict[str, str]) -> List[Tuple[str, float]]:
        if self.is_decision:
            success_prob = self._transition_probabilities[0]
            fail_prob_per_edge = (1 - success_prob) / (len(self._edges) - 1)
            transition_to_edge = policy[self._name]
            transition_to_edge_index = self._edges.index(transition_to_edge)
            transition_probabilities = [
                fail_prob_per_edge for _ in self._edges]
            transition_probabilities[transition_to_edge_index] = success_prob
            return [x for x in zip(self._edges, transition_probabilities)]
        return [x for x in zip(self._edges, self._transition_probabilities)]

    @property
    def edges(self) -> List[str]:
        return self._edges

    @edges.setter
    def edges(self, edges: List[str]) -> None:
        self._edges = edges

    @property
    def transition_probabilities(self) -> List[float]:
        return self._transition_probabilities

    @transition_probabilities.setter
    def transition_probabilities(self, prob: List[float]) -> None:
        self._transition_probabilities = prob

    @property
    def is_decision(self) -> bool:
        return len(self._transition_probabilities) == 1 and len(self._edges) > 1

    @property
    def is_terminal(self) -> bool:
        return len(self._edges) == 0


class TransitionModel:

    def __init__(self, nodes: List[Node]) -> None:
        self._nodes = nodes
        self._node_to_index = {x.name: i for i, x in enumerate(nodes)}
        self._rewards = np.array([x.reward for x in nodes])

    def probability_matrix(self, policy: Dict[str, str]) -> npt.NDArray:
        size = len(self._nodes)
        matrix = np.zeros(shape=[size, size])
        for i, row in enumerate(matrix):
            node = self._nodes[i]
            transition_prob = node.calculate_transition_probabilities(policy)
            for (edge, trans_prob) in transition_prob:
                transition_index = self._node_to_index[edge]
                row[transition_index] = trans_prob
        return matrix

    @property
    def rewards(self) -> npt.NDArray:
        return self._rewards

    @property
    def nodes(self) -> List[Node]:
        return self._nodes

    @staticmethod
    def from_file(file: str) -> 'TransitionModel':
        input = open(file, 'r')
        lines = input.readlines()
        input.close()
        lines = [x for x in lines if not x.isspace()]
        lines = [x for x in lines if not x.startswith('#')]
        rewards = [x.split('=') for x in lines if '=' in x]
        edges = [x.split(':') for x in lines if ':' in x]
        probabilities = [x.split('%') for x in lines if '%' in x]
        rewards = [(x.strip(), y.strip()) for (x, y) in rewards]
        edges = [(x.strip(), y.strip()) for (x, y) in edges]
        probabilities = [(x.strip(), y.strip()) for (x, y) in probabilities]
        all_nodes = set([x[0] for x in (rewards + edges + probabilities)])
        nodes = {x: Node(x) for x in all_nodes}
        edge_defined_nodes = []
        for from_node, to in edges:
            if from_node not in nodes:
                continue
            edge_parsed = [x.strip() for x in to[1:-1].split(',')]
            edge_parsed = [x for x in edge_parsed if not x.isspace()]
            nodes[from_node].edges = edge_parsed
            edge_defined_nodes += edge_parsed
        for node, reward in rewards:
            if node not in nodes:
                continue
            reward_value = float(reward)
            nodes[node].reward = reward_value
        for node, probability in probabilities:
            if node not in nodes:
                continue
            transitional_probabilities = [
                float(x) for x in probability.split()]
            nodes[node].transition_probabilities = transitional_probabilities
        nodes_list = [x for x in nodes.values()]
        nodes_list.sort(key=lambda x: x.name)
        # If a node has edges but no probability entry, it is assumed to be a decision node with p=1
        for node in nodes_list:
            if len(node.transition_probabilities) == 0 and len(node.edges) > 0:
                node.transition_probabilities = [1.0]
        # Iterate through all the nodes and do validation
        if not all_nodes.issuperset(set(edge_defined_nodes)):
            not_found = ' '.join(
                [x for x in set(edge_defined_nodes) - all_nodes])
            raise ParseException(
                'Nodes {} defined in edge entry but not defined elsewhere'.format(not_found))
        TransitionModel._validate(nodes_list)
        return TransitionModel(nodes_list)

    @staticmethod
    def _validate(nodes: List[Node]) -> None:
        for node in nodes:
            if node.is_decision:
                continue
            elif node.is_terminal:
                if len(node.transition_probabilities) != 0:
                    raise ParseException(
                        'Terminal node {} has transition probabilities'.format(
                            node.name)
                    )
            else:
                if len(node.transition_probabilities) != len(node.edges):
                    raise ParseException(
                        'Chance node {} has mismatched edge and probability lengths'.format(node.name))
                if sum(node.transition_probabilities) != 1:
                    raise ParseException(
                        'Chance node {} has total transition probability not equal to 1'.format(
                            node.name)
                    )
