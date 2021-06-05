import argparse
from cmd import CMD

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Runs minimax solver on a DAG file')
    parser.add_argument(
        'type',
        metavar='[min/max]',
        help='Sets root node as min or max')
    parser.add_argument('filename', help='DAG file to solve')
    parser.add_argument(
        '-v',
        '--verbose',
        help='Turns on verbose output mode. Default is false',
        action='store_true',
        default=False)
    parser.add_argument(
        '-ab',
        '--alpha-beta',
        help='Turns on alpha beta pruning. Default is false',
        action='store_true',
        default=False)
    args = parser.parse_args()
    CMD(args.filename, args.type, args.alpha_beta, args.verbose).execute()
