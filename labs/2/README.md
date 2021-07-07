# Requirements 
Needs Python3.8 or higher to run. On CIMS machines, use `python3.8` or `python3.9` 

## Overview

`solver.py` will solve a CNF file

`convert.py` will convert a file with propositional logic to CNF.
The parser does not handle parenthesis, even though the actual
converter logic works off of ASTs and is agnostic parser.


## Other files

`propositional_ast.py` contains much of the actual logic for converting
propositional logic to CNF.

`propositional_parser.py` contains the parser, which parses the file into an AST.
It doesn't handle parenthesis.

`literal.py` is just a small CNF utility file.
