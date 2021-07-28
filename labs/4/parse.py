from typing import Dict, Generator, List, Tuple


class Parser:

    def __init__(self, file: str) -> None:
        self._file = file

    def read_file(self) -> Dict[str, List[str]]:
        with open(self._file, 'r') as input:
            lines = input.readlines()

        def paragrapher(lines: List[str]) -> Generator[Tuple[int, int], None, None]:
            start = 0
            for index in range(len(lines)):
                if lines[index].isspace():
                    yield (start, index)
                    start = index

        paragraphs = [[z.strip() for z in lines[x:y] if not z.isspace()]
                      for x, y in paragrapher(lines)]
        return {name: bio for name, *bio in filter(lambda x: len(x) > 0, paragraphs)}


if __name__ == '__main__':
    output = Parser('input.test').read_file()
    print(output)
