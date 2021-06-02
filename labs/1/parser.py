from node import Node
from typing import Tuple, List, Dict, FrozenSet
from random import shuffle
from os import linesep

class ParserException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Parser:

    def generate_from_file(self, filename: str) -> Node:
        """
        generate_from_file takes in a file, parses it and returns the root node.
        """
        all_nodes = {}
        nodes_with_children = {}
        with open(filename, 'r') as file:
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
        return self._construct_graph(all_nodes, nodes_with_children)

    def _construct_graph(
            self, all_nodes: Dict[str, Node], nodes_with_children: Dict[str, FrozenSet[str]]) -> Node:
        """
        Constructs the graph from the parsed file
        Does cycle detection
        """
        try:
            nodes_with_parents = set()
            for label in nodes_with_children.keys():
                node = all_nodes[label]
                children_labels = nodes_with_children[label]
                children_nodes = [all_nodes[x] for x in children_labels]
                node.children = children_nodes
                nodes_with_parents = nodes_with_parents | children_labels
            root_set = set(all_nodes.keys()) - nodes_with_parents
            if len(root_set) != 1:
                raise ParserException('Root node not found')
            root_node = all_nodes[root_set.pop()]
            self._check_cycle(root_node, set())
            return root_node
        except KeyError as e:
            raise ParserException from e
        
    def _check_cycle(self, start: Node, seen_nodes: FrozenSet[str]) -> None:
        """
        Check the graph for cycles using a DFS
        """
        if start.label in seen_nodes:
            raise ParserException('Cycle detected')
        if start.is_leaf is not True:
            for child in start.children:
                updated_nodes = seen_nodes.union([start.label])
                self._check_cycle(child, updated_nodes)
    
        
    
    def write_to_file(self, root: Node, filename: str, shuffle_output: bool = False) -> None:
        """
        Serialize the tree to a file.
        For variety, set shuffle_output to true
        """
        data = self._traverse_tree_for_write(root)
        if shuffle_output:
            shuffle(data)
        to_write = linesep.join(data)
        with open(filename, 'w') as file:
            file.write(to_write)
    
    def _traverse_tree_for_write(self, start: Node) -> List[str]:
        return_val = []
        if start is None:
            return return_val
        if start.is_leaf:
            output_str = '{}={}'.format(start.label, start.value)
            return_val.append(output_str)
        else:
            children = '[{}]'.format(', '.join([x.label for x in start.children]))
            output_str = '{}: {}'.format(start.label, children)
            return_val.append(output_str)
            for x in start.children:
                return_val.extend(self._traverse_tree_for_write(x))
        
        return return_val

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
