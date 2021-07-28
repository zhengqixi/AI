from typing import Dict, List, Set
from functools import reduce
from math import log2


class Cluster:

    class _Node:

        def __init__(self, bio: str, weight: float) -> None:
            self.bio = bio
            self.weight = weight
            self.connections = set()

    def __init__(self, processed_bios: Dict[str, Set[str]], stem_to_words : Dict[str, str]) -> None:
        self._bios = processed_bios
        self._stem_to_words = stem_to_words
        word_weights = self._weights()
        self._node_weights = {bio: sum([word_weights[word]
                                  for word in words]) for bio, words in self._bios.items()}
        self._word_weights = word_weights

    def cluster(self, N: float) -> Dict[str, List[str]]:
        nodes = [self._Node(bio, self._node_weights[bio]) for bio in self._bios.keys()]
        self._connect_nodes(N, nodes)
        visited = set()
        L = []
        for node in nodes:
            self._visit(node, L, visited)
        components = {}
        for node in L:
            self._assign(node, node, components, set())
        reassigned_names = {self._determine_cluster_name(clustered): clustered for _, clustered in components.items()}
        return reassigned_names 
    
    def _determine_cluster_name(self, values: List[str]) -> str:
        all_words = reduce(lambda x,y : x.union(y), [self._bios[x] for x in values])
        word_weights = [(word, self._word_weights[word]) for word in all_words]
        word_weights.sort(key=lambda x : x[1])
        return ' '.join([x[0].capitalize() for x in word_weights[:2]])
    
    def _assign(self, node: _Node, root: _Node, components: Dict[str, List[str]], assigned: Set[str])-> None:
        if node.bio in assigned:
            return
        if root.bio not in components:
            components[root.bio] = [node.bio]
        else:
            components[root.bio].append(node.bio)
        assigned.add(node.bio)
        for connection in node.connections:
            self._assign(connection, root, components, assigned)
    
    def _visit(self, node: _Node, L: List[_Node], visited: Set[str]) -> None:
        if node.bio in visited:
            return
        visited.add(node.bio)
        L.append(node)
        for connection in node.connections:
            self._visit(connection, L, visited)

    
    def _connect_nodes(self, N: float, nodes: List[_Node]) -> None:
        for a in nodes:
            for b in nodes:
                if a in b.connections:
                    continue
                if a.weight + b.weight > N:
                    a.connections.add(b)
                    b.connections.add(a)


    def _weights(self) -> Dict[str, float]:
        all_words = reduce(lambda x, y: x.union(y), self._bios.values())
        return {word: self._word_weight(word) for word in all_words}

    def _word_weight(self, word: str) -> float:
        occurances = sum([1 for x in self._bios.values() if word in x])
        return -log2(occurances/len(self._bios))

if __name__ == '__main__':
    from parse import Parser
    from processor import Processor
    parser = Parser('input.test')
    processor = Processor(parser.read_file(), set(['with', 'from', 'later']))
    cluster = Cluster(processor.process(), processor.stem_to_words)
    print(cluster.cluster(160))
