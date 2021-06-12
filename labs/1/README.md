# Requirements
Needs Python3.8 or higher to run. On CIMS machines, use `python3.8` or `python3.9`

## Overview
`minimax.py` contains the main command line tool for the minimax solver.
Use something like `python3 minimax.py` to run it. 


`generator.py` contains the tic tac toe graph generator.
When using it, provide the name of the file to write the DAG to.
Something like `python3 generator.py` should work.

## Other files

`cmd.py` contains some wrappers and other utilities for the `minimax.py`.
In theory they could've just been one file, but whatever.

`generator.py` contains the recursive traversal logic for tic tac toe DAG generation 

`minimax.py` I already explained

`node.py` defines the node struct used throughout this assignment

`parser.py` parses a DAG file into an in memory graph, and can write
an in memory graph to a DAG file

`README.md` this

`solver.py` contains the logic for minimax and alpha-beta solving

`tictactoe.py` contains the representation of the tic tac toe board
and functions for manipulating said board
