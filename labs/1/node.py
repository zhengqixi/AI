from typing import List


class NodeException(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Node:

    """
    Node represents a node in the DAG
    """

    def __init__(self, label: str, value: int = None,
                 children: List['Node'] = None) -> None:
        self._label = label
        self._value = value
        self._children = children

    @property
    def label(self) -> str:
        return self._label
    
    @label.setter
    def label(self, label: str) -> None:
        self._label = label

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int) -> None:
        self._value = value

    @property
    def is_leaf(self) -> bool:
        return self._children is None

    @property
    def children(self) -> List['Node']:
        return self._children

    @children.setter
    def children(self, children: List['Node']) -> None:
        self._children = children
