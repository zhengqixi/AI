from typing import List, Tuple
class TransitionModel:
    def __init__(self, rewards: List[Tuple[str, float]], transitions: List[Tuple[str, List[Tuple[str, float]]]]) -> None:
        self._rewards = {x[0]:x[1] for x in rewards}
        all_states = [x[0] for x in rewards]
        self._states_index = {x[0]:x[1] for x in zip(all_states, range(len(all_states)))}
        self._index_to_states = {x[1]:x[0] for x in zip(all_states, range(len(all_states)))}
        self._transition_matrix = [[0.0 for _ in range(len(all_states))] for _ in range(len(all_states))]
        for from in transitions:
            for to in from[1]:
                from_index = self._states_index[from[0]]
                to_index = self._states_index[to[0]]
                self._transition_matrix[from_index][to_index] = to[1]
        self._all_states = all_states

    def reward(self, state: str) -> float:
        return self._rewards[state]
    
    def transition_probability(self, to: str, from: str) -> float:
        from_index = self._states_index[from]
        to_index = self._states_index[to]
        return self._transition_matrix[from_index][to_index]

    def all_to_state(self, to: str) -> List[Tuple[str, float]]:
        to_index = self._states_index[to]
        column = [self._transition_matrix[i][to_index] for i in range(len(self._states_index))]
        return [[self._index_to_states[i],prob] for i, prob in enumerate(column) if prob != 0]
    
    def all_from_state(self, from: str) -> List[Tuple[str, float]]:
        from_index = self._states_index[from]
        return [[self._index_to_states[i],prob] for i, prob in enumerate(self._transition_matrix[from_index]) if prob != 0]
