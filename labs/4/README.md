# Requirements 
Needs Python3.8 or higher to run. On CIMS machines, use `python3.8` or `python3.9` 

## Overview

`python3 cmd.py -h` to see instructions. Basically implements the commands asked for.


## Other files

`cluster.py` does the actual clustering, implementing the algorithm described.
To determine strongly connected components, Kosaraju's algorithm is used.
K means was not chosen, as there was no described way
to transform the texts onto a n-dimensional space in a way
that really made sense.

`parse.py` parses the biographies. Does not do any kind of preprocessing.

`processor.py` contains all of the actual preprocessing. 

`stemmer.py` is the stemmer used. Taken from https://tartarus.org/martin/PorterStemmer/python.txt
