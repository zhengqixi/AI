from typing import List, Tuple
from literal import Literal
from itertools import chain
import argparse


class SolverParser():

    @staticmethod
    def parse(file: str) -> List[List[Literal]]:
        with open(file, 'r') as input:
            lines = [list(filter(None, x.split())) for x in input]
            lines = [x for x in lines if len(x) != 0]

            def to_literal(value: str) -> Literal:
                if value[0] == '!':
                    return Literal(value[1:], True)
                return Literal(value)
            return [list(map(to_literal, y)) for y in lines]


class Solver():

    @staticmethod
    def solve(input: List[List[Literal]]) -> List[Tuple[str, bool]]:
        """
        Returns a list of all evaluates values.
        If there is no way to satisfy the constraints, return None
        """
        start = Solver._determine_guess(input)
        result = Solver._solve_step(input, start[1][0], start[1][1])
        if result is None:
            negated = not start[1][1]
            result = Solver._solve_step(input, start[1][0], negated)
        return result

    @staticmethod
    def _solve_step(sentences: List[List[Literal]],
                    atom: str, value: bool) -> List[Tuple[str, bool]]:
        """
        Returns a list of all evaluates values.
        If there is an error, returns none
        """
        # Copy and filter out False literals
        evaluated = [[Literal(y.atom, y.negation) for y in x if y.evaluate(
            atom, value) != False] for x in sentences]
        # Check for empty values. If they exist, we cannot continue down this
        # path
        for sentence in evaluated:
            if len(sentence) == 0:
                return None
        # Filter out sentences which have been completed.
        copied = []
        for sentence in evaluated:
            new_sentence = []
            for literal in sentence:
                evaluated = literal.evaluate(atom, value)
                if evaluated == True:
                    # Because all sentences are ORs, only one value needs to be true for the sentence to be true
                    # This sets the new sentence length to zero, essentially
                    # removing it
                    new_sentence = []
                    break
                if evaluated is None:
                    new_sentence.append(literal)
            if len(new_sentence) != 0:
                copied.append(new_sentence)
        if len(copied) == 0:
            return [[atom, value]]
        decision = Solver._determine_guess(copied)
        result = Solver._solve_step(copied, decision[1][0], decision[1][1])
        if result is None and decision[0]:
            # We guessed based on a literal
            # Guessing the negation means that the literal has to be unsatisfiable
            # We need to further backtrack
            return None
        if result is None:
            # We can try again
            negated_guess = not decision[1][1]
            result = Solver._solve_step(copied, decision[1][0], negated_guess)
        if result is None:
            return None
        result.append([atom, value])
        return result

    @staticmethod
    def _determine_guess(
            sentences: List[List[Literal]]) -> Tuple[bool, Tuple[str, bool]]:
        """
        Determines which value to guess
        First bool is true if it is a literal
        If not, we pick the lowest lexicographic order atom
        And guess True
        """
        literals = [x[0] for x in sentences if len(x) == 1]
        if len(literals) != 0:
            literals.sort(key=lambda x: x.atom)
            selected = literals[0]
            if selected.negation:
                return [True, [selected.atom, False]]
            return [True, [selected.atom, True]]
        atoms = [atom for atom in chain.from_iterable(sentences)]
        atoms.sort(key=lambda x: x.atom)
        selected = atoms[0]
        return [False, [selected.atom, True]]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solves a CNF input file'
    )
    parser.add_argument('filename', help='CNF input file')
    args = parser.parse_args()
    file = args.filename
    sentences = SolverParser.parse(file)
    result = Solver.solve(sentences)
    if result is None:
        print('NO VALID ASSIGNMENT')
        exit() 
    result.sort(key=lambda x: x[0])
    for i in result:
        print('{}={}'.format(i[0], i[1]))
