from typing import List
from propositional_ast import PropositionalAST

class Parser:
    def __init__(self, file: str) -> None:
        self._file = file
    
    def parse(self) -> List[PropositionalAST]:
        pass
