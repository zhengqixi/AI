from typing import List
from propositional_ast import NegateOperator, PropositionalAST, BinaryOperator, BinaryPropositionalOperator, Atom
from propositional_parser import Parser
from literal import Literal
from itertools import chain
import argparse


class ConvertException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Root:
    def __init__(self, children: List[PropositionalAST]) -> None:
        self._children = children

    def _to_cnf(self) -> List[PropositionalAST]:
        return [x.to_cnf() for x in self._children]

    def to_literals(self) -> List[List[Literal]]:
        children = self._to_cnf()
        results = [self._to_literals(x) for x in children]
        literals = [x for x in chain.from_iterable(results)]
        # Sort literals in order
        for x in literals:
            x.sort(key=lambda x: x.atom)
        # Use dictionary to remove duplicates
        filtered = {''.join([str(y) for y in x]): x for x in literals}
        filtered_literals = [x for x in filtered.values()]
        return filtered_literals

    def _to_literals(self, node: PropositionalAST) -> List[List[Literal]]:
        if isinstance(node, Atom):
            return [[Literal(node.atom)]]
        if isinstance(node, NegateOperator):
            if not isinstance(node.child, Atom):
                raise ConvertException(
                    'Should not have negate operators with non atoms')
            return [[Literal(node.child.atom, negation=True)]]
        if isinstance(node, BinaryOperator):
            left = self._to_literals(node.left)
            right = self._to_literals(node.right)
            if node.operator == BinaryPropositionalOperator.OR:
                # We take the left and right results, and append together
                # to form one sentence
                return [left[0] + right[0]]
            elif node.operator == BinaryPropositionalOperator.AND:
                return left + right
            else:
                raise ConvertException(
                    'Should not have non AND/OR BinaryOperators')
        raise ConvertException(
            'There are literally no other types defined...how can???')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts propositional logic to a CNF file'
    )
    parser.add_argument('filename', help='Propositional logic input file')
    args = parser.parse_args()
    file = args.filename
    parser = Parser(file)
    root = Root(parser.parse())
    result = root.to_literals()
    for sentence in result:
        print(' '.join(str(x) for x in sentence))
