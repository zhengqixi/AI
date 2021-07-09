from typing import Dict, List, Tuple
import numpy.typing as npt
import numpy as np

class TransitionModel:

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
                transition_probabilities = [fail_prob_per_edge for _ in self._edges] 
                transition_probabilities[transition_to_edge_index] = success_prob
                return [x for x in zip(self._edges, transition_probabilities)]
            return [x for x in zip(self._edges, self._transition_probabilities)]

        @property
        def edges(self) -> List[str] :
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
            return len(self._transition_probabilities) == 1
        
        @property
        def is_terminal(self) -> bool:
            return len(self._edges) == 0
        
    
    def __init__(self, nodes: List[Node]) -> None:
        self._nodes = nodes
        self._node_to_index = {x.name:i for i, x in enumerate(nodes)}
        self._rewards = np.array([x.reward for x in nodes])


    def probability_matrix(self, policy: Dict[str, str]) -> npt.NDArray:
        size = len(self._nodes)
        matrix = np.zeros(shape=[size,size])
        for i, row in enumerate(matrix):
            node = self._nodes[i]
            transition_prob = node.calculate_transition_probabilities(policy)
            for edge in transition_prob:
                transition_index = self._node_to_index[edge[0]]
                row[transition_index] = edge[1]
        return matrix

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
        rewards = [x.split('=') for x in lines if '=' in x]
        edges = [x.split(':') for x in lines if ':' in x]
        probabilities = [x.split('%') for x in lines if '%' in x]
        rewards= [[x[0].strip(), x[1].strip()] for x in rewards]
        edges = [[x[0].strip(), x[1].strip()] for x in edges]
        probabilities = [[x[0].strip(), x[1].strip()] for x in probabilities]
        all_nodes = set([x[0] for x in (rewards + edges + probabilities)])
        nodes = {x: TransitionModel.Node(x) for x in all_nodes}
        for reward in rewards:
            node = reward[0]
            if node not in nodes:
                continue
            reward_value = float(reward[1])
            nodes[node].reward = reward_value
        for probability in probabilities:
            node = probability[0]
            if node not in nodes:
                continue
            transitional_probabilities = [float(x) for x in probability[1].split()]
            nodes[node].transition_probabilities = transitional_probabilities
        for edge in edges:
            node = edge[0]
            if node not in nodes:
                continue
            edge_parsed = [x.strip() for x in edge[1][1:-1].split(',')]
            edge_parsed = [x for x in edge_parsed if not x.isspace()]
            nodes[node].edges = edge_parsed
        # Iterate through all the nodes and do validation
        return TransitionModel([x for x in nodes.values()])

if __name__ == '__main__':
    model = TransitionModel.from_file('test1.test')
    nodes = model.nodes
    print(nodes)
    policy = {'B': 'A'}
    transition = model.probability_matrix(policy)
    print(transition)
