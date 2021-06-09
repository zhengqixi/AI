from enum import Enum
from typing import List, Tuple


class TileState(Enum):
    X = 1
    O = -1
    EMPTY = 0


class TicTacToeBoard:
    def __init__(self) -> None:
        self._board = [[TileState.EMPTY for _ in range(3)] for _ in range(3)]

    def set(self, row: int, column: int, state: TileState) -> None:
        self._board[row][column] = state

    def empty_tiles(self) -> List[Tuple[int, int]]:
        empty_tiles = []
        for row in range(3):
            for column in range(3):
                if self._board[row][column] == TileState.EMPTY:
                    empty_tiles.append([row, column])
        return empty_tiles

    def check_win(self, player: TileState) -> bool:
        for i in range(3):
            if self._check_list(self._board[i], player):
                return True
            if self._check_column(i, player):
                return True
        diagonal = [self._board[row][column]
                    for row in range(3) for column in range(3)]
        if self._check_list(diagonal, player):
            return True
        diagonal = [self._board[row][column]
                    for row in range(3) for column in range(2, -1, -1)]
        if self._check_list(diagonal, player):
            return True
        return False

    def _check_list(self, data: List[TileState], player: TileState) -> bool:
        return len([x for x in data if x == player]) == len(data)

    def _check_column(self, column: int, player: TileState) -> bool:
        return self._check_list(self._get_column(column), player)

    def _copy(self) -> 'TicTacToeBoard':
        new_board = TicTacToeBoard()
        for row in range(3):
            for column in range(3):
                new_board._board[row][column] = self._board[row][column]
        return new_board

    def _set_row(self, row_num: int, row: List[TileState]) -> None:
        self._board[row_num] = row

    def _get_row(self, row_num: int) -> List[TileState]:
        return self._board[row_num].copy()

    def _set_column(self, column_num: int,
                    column: List[TileState]) -> None:
        for i in range(3):
            self._board[i][column_num] = column[i]

    def _get_column(self, column_num: int) -> List[TileState]:
        return [self._board[x][column_num] for x in range(3)]

    def x_flip(self) -> 'TicTacToeBoard':
        """
        Create a copy of the current board, and flip along the x-axis
        This is done by swapping the following (row, column) pairs:
        (0,0) <-> (2,0)
        (0,1) <-> (2,1)
        (0,2) <-> (2,2)
        """
        new_board = self._copy()
        new_board._board[0][0], new_board._board[2][0] = new_board._board[2][0], new_board._board[0][0]
        new_board._board[0][1], new_board._board[2][1] = new_board._board[2][1], new_board._board[0][1]
        new_board._board[0][2], new_board._board[2][2] = new_board._board[2][2], new_board._board[0][2]
        return new_board

    def y_flip(self) -> 'TicTacToeBoard':
        """
        Create a copy of the current board, and flip along the y-axis
        This is done by swapping the following (row, column) pairs:
        (0,0) <-> (0,2)
        (1,0) <-> (1,2)
        (2,0) <-> (2,2)
        """
        new_board = self._copy()
        new_board._board[0][0], new_board._board[0][2] = new_board._board[0][2], new_board._board[0][0]
        new_board._board[1][0], new_board._board[1][2] = new_board._board[1][2], new_board._board[1][0]
        new_board._board[2][0], new_board._board[2][2] = new_board._board[2][2], new_board._board[2][0]
        return new_board

    def rotate_ccw_90(self) -> 'TicTacToeBoard':
        new_board = self._copy()
        new_board._rotate_ccw_90()
        return new_board

    def _rotate_ccw_90(self) -> None:
        left_column = self._get_column(0)
        bottom_row = self._get_row(2)
        right_column = self._get_column(2)
        top_row = self._get_row(0)
        self._set_row(2, left_column)
        bottom_row.reverse()
        self._set_column(2, bottom_row)
        self._set_row(0, right_column)
        top_row.reverse()
        self._set_column(0, top_row)

    def rotate_ccw_180(self) -> 'TicTacToeBoard':
        new_board = self.rotate_ccw_90()
        new_board._rotate_ccw_90()
        return new_board

    def rotate_ccw_270(self) -> 'TicTacToeBoard':
        new_board = self.rotate_ccw_180()
        new_board._rotate_ccw_90()
        return new_board

    def rotate_cw_90(self) -> 'TicTacToeBoard':
        """
        Create a copy of the current board, and rotates cw 90
        """
        new_board = self._copy()
        new_board._rotate_cw_90()
        return new_board

    def _rotate_cw_90(self) -> None:
        """
        Rotates self cw 90
        """
        left_column = self._get_column(0)
        bottom_row = self._get_row(2)
        right_column = self._get_column(2)
        top_row = self._get_row(0)
        left_column.reverse()
        self._set_row(0, left_column)
        self._set_column(2, top_row)
        right_column.reverse()
        self._set_row(2, right_column)
        self._set_column(0, bottom_row)

    def rotate_cw_180(self) -> 'TicTacToeBoard':
        """
        Create a copy of the current board, and rotates cw 180
        """
        new_board = self.rotate_cw_90()
        new_board._rotate_cw_90()
        return new_board

    def rotate_cw_270(self) -> 'TicTacToeBoard':
        new_board = self.rotate_cw_180()
        new_board._rotate_cw_90()
        return new_board

    def hash(self) -> str:
        flattened = [*self._board[0], *self._board[1], *self._board[2]]
        flattened_str = [str(x) for x in flattened]
        return ';'.join(flattened_str)


if __name__ == '__main__':
    board = TicTacToeBoard()
    board.set(0, 0, TileState.X)
    board.set(1, 0, TileState.X)
    board.set(2, 0, TileState.X)
    board.set(2, 1, TileState.O)
    board.set(2, 2, TileState.O)
    board2 = board.rotate_ccw_90()
    board3 = board.rotate_cw_90()
    board4 = board3.rotate_cw_90()
    print('over')
