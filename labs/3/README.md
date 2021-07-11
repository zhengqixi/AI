# Requirements
`Python3.8 or higher. GNU make utility`

# Usage
First, type `make`. This sets up the virtual environment and installs the necessary packages.

`mdp` can be executed with the arguments defind in the assignment.

# Overview

`cmd.py` does command line parsing and puts everything together.

`model.py` parses the file, and creates a model which can be used to determine transition probability matrices given a policy.

`solver.py` implements the policy iteration algorithm.

`mdp` is a bash script meant for convenience.
