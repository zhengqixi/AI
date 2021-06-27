from typing import List, Tuple
from propositional_ast import BinaryOperator, PropositionalAST, PropositionalOperators, BinaryPropositionalOperator, SingularPropositionalOperator, NegateOperator, Atom
from collections import deque


class ParserException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Parser:
    LEFT_PARENTHESIS = '('
    RIGHT_PARENTHESIS = ')'
    ALL_TOKENS = [LEFT_PARENTHESIS, RIGHT_PARENTHESIS] + \
        [x.value for x in PropositionalOperators]
    BREAK_TOKENS = set([x[0] for x in ALL_TOKENS])
    IMMEDIATE_PUSH_TOKEN = set([x for x in ALL_TOKENS if len(x) == 1])
    LOOKAHEAD_NEEDED_TOKEN = {x[0]: x for x in ALL_TOKENS if len(x) > 1}
    ENUM_VALUE_TO_ENUM = {x.value: x for x in PropositionalOperators}

    def __init__(self, file: str) -> None:
        self._file = file

    def parse(self) -> List[PropositionalAST]:
        with open(self._file, 'r') as input:
            lines = [y for y in filter(None, [x.strip() for x in input])]
            return [x for x in map(self._parse_line, lines)]

    def _parse_line(self, line: str) -> PropositionalAST:
        tokens = self._parse_to_tokens(line)
        return self._parse_tokens(tokens)
    
    def _parse_tokens(self, line: List[str]) -> PropositionalAST:
        top = self._find_lowest_binary_operator(line)
        if top is not None:
            operator = self.ENUM_VALUE_TO_ENUM[top[0].value]
            left = self._parse_tokens(top[1])
            right = self._parse_tokens(top[2])
            return BinaryOperator(operator, left, right)
        if len(line) == 2:
            if line[0] == SingularPropositionalOperator.NOT.value and line[1].isalnum():
                return NegateOperator(Atom(line[1])) 
            else:
                raise ParserException('{} is not valid'.format(line))
        if len(line) == 1:
            if line[0].isalnum():
                return Atom(line[0])
        raise ParserException('{} is not valid'.format(line))

    def _parse_to_tokens(self, line: str) -> List[str]:
        tokens = []
        queue = deque(line)
        accumulator = ''
        while len(queue) != 0:
            token = queue.popleft()
            if token.isspace() or token in self.BREAK_TOKENS:
                if len(accumulator) > 0:
                    tokens.append(accumulator)
                    accumulator = ''
            if token.isspace():
                continue
            elif token in self.IMMEDIATE_PUSH_TOKEN:
                tokens.append(token)
            elif token in self.LOOKAHEAD_NEEDED_TOKEN:
                to_match = self.LOOKAHEAD_NEEDED_TOKEN[token]
                if (len(to_match) - 1) > len(queue):
                    raise ParserException(
                        'Not enough tokens to create {}'.format(to_match))
                for _ in range(len(to_match) - 1):
                    token += queue.popleft()
                if token != to_match:
                    raise ParserException(
                        'Invalid token detected: {}'.format(token))
                tokens.append(token)
            elif token.isalnum():
                accumulator += token
            else:
                raise ParserException(
                    'Invalid token detected: {}'.format(token))
        if len(accumulator) > 0:
            tokens.append(accumulator)
        return tokens

    def _find_lowest_binary_operator(
            self, line: List[str]) -> Tuple[str, List[str], List[str]]:
        for operator in BinaryPropositionalOperator:
            index = next((i for i in reversed(range(len(line)))
                          if line[i] == operator.value), -1)
            if index != -1:
                return [operator, line[:index], line[index + 1:]]
        return None
