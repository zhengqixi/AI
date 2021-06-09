from tictactoe import TicTacToeBoard
from tictactoe import TileState
from node import Node
from parser import Parser


class Generator:
    _min_level = 6
    _row_str = ['1', '2', '3']
    _column_str = ['a', 'b', 'c']

    def __init__(self, starting_player: TileState) -> None:
        self._starting_player = starting_player
        self._cache = {}

    def generate(self) -> Node:
        board = TicTacToeBoard()
        root = Node('')
        self._level(root, board, self._starting_player, 0)
        root.label = 'root'
        return root

    def _level(self, parent: Node, board: TicTacToeBoard,
               player: TileState, level: int) -> None:
        other_player = self._switch_player(player)
        if level >= self._min_level:
            if board.check_win(other_player):
                parent.value = self._value(other_player)
                return
        moves = board.empty_tiles()
        if len(moves) == 0:
            parent.value = self._value(TileState.EMPTY)
            return
        parent_label = parent.label
        children = []
        for move in moves:
            board.set(move[0], move[1], player)
            child_node = self._check_cache(board)
            if child_node is not None:
                children.append(child_node)
            else:
                child_label = parent_label + self._notation(move[0], move[1])
                child_node = Node(child_label)
                children.append(child_node)
                self._cache_board(board, child_node)
                self._level(child_node, board, other_player, level + 1)
            board.set(move[0], move[1], TileState.EMPTY)
        parent.children = [x for x in {x.label: x for x in children}.values()]

    def _switch_player(self, player: TileState) -> TileState:
        if player == TileState.X:
            return TileState.O
        if player == TileState.O:
            return TileState.X
        raise Exception('bruhhhh')

    def _notation(self, row: int, column: int) -> str:
        return self._column_str[column] + self._row_str[row]

    def _value(self, player: TileState) -> int:
        if player == TileState.X:
            return 1
        elif player == TileState.O:
            return -1
        elif player == TileState.EMPTY:
            return 0
        raise Exception('bruuhh')

    def _check_cache(self, board: TicTacToeBoard) -> Node:
        hash = board.hash()
        if hash in self._cache:
            return self._cache[hash]
        return None

    def _cache_board(self, board: TicTacToeBoard, node: Node) -> None:
        self._cache[board.hash()] = node
        self._cache[board.x_flip().hash()] = node
        self._cache[board.y_flip().hash()] = node
        self._cache[board.rotate_ccw_90().hash()] = node
        self._cache[board.rotate_ccw_180().hash()] = node
        self._cache[board.rotate_ccw_270().hash()] = node
        self._cache[board.rotate_cw_90().hash()] = node
        self._cache[board.rotate_cw_180().hash()] = node
        self._cache[board.rotate_cw_270().hash()] = node


if __name__ == '__main__':
    root = Generator(TileState.X).generate()
    parser = Parser()
    parser.write_to_file(root, 'nice.test')
