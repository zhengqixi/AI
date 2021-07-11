from typing import Dict, Tuple, List
import numpy.typing as npt
import numpy as np
from model import TransitionModel, Node


class Solver:

    def __init__(self, model: TransitionModel, discount: float, value_iter: int, value_tolerance: float, min: bool) -> None:
        self._discount = discount
        self._model = model
        self._value_iter = value_iter
        self._value_tolerance = value_tolerance
        self._min = min

    def solve(self) -> Tuple[Dict[str, str], npt.NDArray]:
        nodes = self._model.nodes
        nodes_to_index = {x.name: i for i, x in enumerate(nodes)}
        v = self._model.rewards
        decision_nodes = [x for x in nodes if x.is_decision]
        # Initial policy is arbitrary
        policy = {x.name: x.edges[0] for x in decision_nodes}
        while True:
            v = self._value_iterate(policy, v)
            updated_policy = False
            for node in decision_nodes:
                current_policy = policy[node.name]
                best_policy = self._calculate_best_policy(
                    node, v, nodes_to_index)
                if current_policy != best_policy:
                    policy[node.name] = best_policy
                    updated_policy = True

            if not updated_policy:
                return [policy, v]

    def _value_iterate(self, policy: Dict[str, str], v: npt.NDArray) -> npt.NDArray:
        probability_matrix = self._model.probability_matrix(policy)
        rewards = self._model.rewards
        new_v = v
        for _ in range(self._value_iter):
            new_v = rewards + self._discount * np.matmul(probability_matrix, v)
            max_diff = np.max(np.absolute(new_v))
            if max_diff <= self._value_tolerance:
                return new_v
            v = new_v
        return new_v

    def _calculate_best_policy(self, node: Node, v: List[float], nodes_to_index: Dict[str, int]) -> str:
        success_prob = node.transition_probabilities[0]
        fail_prob_per_edge = (1 - success_prob) / (len(node.edges) - 1)
        rewards = []
        for policy in node.edges:
            policy_reward = success_prob * v[nodes_to_index[policy]]
            other_rewards = node.edges.copy()
            other_rewards.remove(policy)
            other_rewards_sum = [v[nodes_to_index[x]] *
                                 fail_prob_per_edge for x in other_rewards]
            rewards.append((policy, policy_reward + sum(other_rewards_sum)))
        if self._min:
            return min(rewards, key=lambda x: x[1])[0]
        return max(rewards, key=lambda x: x[1])[0]
