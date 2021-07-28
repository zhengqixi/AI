import argparse
from typing import Set, Union
from parse import Parser
from processor import Processor
from cluster import Cluster
from functools import reduce

def read_stopwords(file: Union[str, None]) -> Set[str]:
    if file is None:
        return set()
    with open(file, 'r') as stopwords:
        words = [[y.strip().lower() for y in x.split()] for x in stopwords]
        return set(reduce(lambda x, y : x + y, words))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Cluster some biographies"
    )
    parser.add_argument('filename', help='Input biography file')
    parser.add_argument(
        '-N',
        help='N value for clustering algorithm. Defaults to 150.',
        type=float,
        default=150.0
    )
    parser.add_argument(
        '-s',
        help='Stopwords that will be removed from clustering algorithm'
    )
    args = parser.parse_args()
    filename = args.filename
    N = args.N
    stopwords = read_stopwords(args.s)
    parser = Parser(filename)
    processor = Processor(parser.read_file(), stopwords)
    processed = processor.process()
    cluster = Cluster(processed, processor.stem_to_words)
    for key, values in cluster.cluster(N).items():
        print('{}: {}'.format(key, ', '.join(values)))

