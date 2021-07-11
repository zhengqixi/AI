from solver import Solver
from model import TransitionModel
import argparse


def discount_factor(arg) -> float:
    try:
        value = float(arg)
    except ValueError as err:
        raise argparse.ArgumentTypeError(str(err))
    if value < 0 or value > 1.0:
        raise argparse.ArgumentTypeError(
            'Discount factor must be between 0 and 1')
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Solver for a finite MDP'
    )
    parser.add_argument('filename', help='Inputfile')
    parser.add_argument(
        '-df',
        help='Discount factor',
        type=discount_factor,
        default=1.0
    )
    parser.add_argument(
        '-tol',
        help='Fault tolerance for value iteration',
        type=float,
        default=0.001
    )
    parser.add_argument(
        '-iter',
        help='Iteration limit for value iteration',
        type=int,
        default=50
    )
    parser.add_argument(
        '-min',
        help='If set, will minimize cost instead of maximize reward',
        action='store_true',
        default=False
    )
    args = parser.parse_args()
    model = TransitionModel.from_file(args.filename)
    solver = Solver(model,
                    discount=args.df,
                    value_tolerance=args.tol,
                    value_iter=args.iter,
                    min=args.min
                    )
    policy, values = solver.solve()
    policies = [x for x in policy.keys()]
    policies.sort()
    for x in policies:
        print('{} -> {}'.format(x, policy[x]))
    print(' ')
    nodes = [x.name for x in model.nodes]
    node_values = ['{}={}'.format(name, round(value, 3))
                   for name, value in zip(nodes, values)]
    print(' '.join(node_values))
