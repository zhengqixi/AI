from node import Node
from typing import Tuple, List, Dict, FrozenSet


class ParserException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Parser:

    def __init__(self, filename: str) -> None:
        self._filename = filename

    def generate_from_file(self) -> Node:
        """
        generate_from_file takes in a file, parses it and returns the root node.
        """
        all_nodes = {}
        nodes_with_children = {}
        with open(self._filename, 'r') as file:
            for line in file:
                if ':' in line:
                    node, children = self._parse_internal(line)
                    if node.label in all_nodes:
                        raise ParserException(
                            'node {} duplicate'.format(node.label))
                    all_nodes[node.label] = node
                    nodes_with_children[node.label] = children
                else:
                    node = self._parse_leaf(line)
                    if node.label in all_nodes:
                        raise ParserException(
                            'node {} duplicate'.format(node.label))
                    all_nodes[node.label] = node
        return self._validate_graph(all_nodes, nodes_with_children)

    def _validate_graph(
            self, all_nodes: Dict[str, Node], nodes_with_children: Dict[str, FrozenSet[str]]) -> Node:
        """
        Run validations against the parsed graph
        """
        try:
            nodes_with_parents = set()
            for label in nodes_with_children.keys():
                node = all_nodes[label]
                children_labels = nodes_with_children[label]
                children_nodes = [all_nodes[x] for x in children_labels]
                node.children = children_nodes
                new_nodes_with_parents = nodes_with_parents | children_labels
                if len(new_nodes_with_parents) != (
                        len(nodes_with_parents) + len(children_labels)):
                    # This would mean that there is a duplicate between nodes we've already seen
                    # and a new children label node
                    # likely a cycle
                    raise ParserException('Cycle likely...')
                nodes_with_parents = new_nodes_with_parents
            root_set = set(all_nodes.keys()) - nodes_with_parents
            if len(root_set) != 1:
                raise ParserException('Root node not found')
            return all_nodes[root_set.pop()]
        except KeyError as e:
            raise ParserException from e

    def _parse_leaf(self, line: str) -> Node:
        """
        Parse a leaf node. This will return a node with its label
        """
        split_str = line.split('=')
        if len(split_str) != 2:
            raise ParserException(
                'line {} is invalid for a leaf node'.format(line))
        try:
            value = int(split_str[1])
            return Node(label=split_str[0].strip(), value=value)
        except ValueError as e:
            raise ParserException from e

    def _parse_internal(self, line: str) -> Tuple[Node, FrozenSet[str]]:
        """
        Parse an internal node. This returns a node, with a list of the names
        of its children
        """
        split_str = line.split(':')
        if len(split_str) != 2:
            raise ParserException(
                'line {} is invalid for an internal node'.format(line))
        children_str = split_str[1].strip()
        if len(
                children_str) < 2 or children_str[0] != '[' or children_str[-1:] != ']':
            raise ParserException(
                'children string {} is improperly formatted'.format(children_str))
        children = [x.strip() for x in children_str[1:-1].split(',')]
        children_set = set(children)
        if len(children) != len(children_set):
            raise ParserException(
                '{} has duplicate children'.format(children_str))
        return Node(label=split_str[0].strip()), children_set
