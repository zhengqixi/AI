from typing import List
from propositional_ast import PropositionalAST

class Parser:
    def __init__(self, file: str) -> None:
        self._file = file
    
    def parse(self) -> List[PropositionalAST]:
        with open(self._file, 'r') as input:
            lines = [y for y in filter(None, [x.strip() for x in input])]
            return [x for x in map(self._parse_line, lines)]
    
    def _parse_line(self, line: str) -> PropositionalAST:
        pass
