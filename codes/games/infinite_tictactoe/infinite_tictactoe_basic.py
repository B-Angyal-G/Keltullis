import numpy as np
import copy as c

from numpy.typing import NDArray
from typing import Self

from games.abstract_game import abstract_game
from utils.side import Side




class infinite_tictactoe_basic(abstract_game):
    size : int
    side : Side
    board: NDArray[np.int32]


    def make_move(self, position : tuple[int]) -> Self:     # type: ignore[override]
        next_game = type(self)( self.side.next_player() )
        next_game.board = c.copy(self.board)

        # Kör: 2, 4, 8
        if self.side == Side.FIRST:
            for i in range(9):
                if i == position[0]:
                    next_game.board[i] = 2
                elif self.board[i] == 2 or self.board[i] == 4:
                    next_game.board[i] *= 2
                elif self.board[i] == 8 or self.board[i] == 0:
                    next_game.board[i] = 1

        # X: 16, 32, 64
        if self.side == Side.SECOND:
            for i in range(9):
                if i == position[0]:
                    next_game.board[i] = 16
                elif self.board[i] == 16 or self.board[i] == 32:
                    next_game.board[i] *= 2
                elif self.board[i] == 64 or self.board[i] == 0:
                    next_game.board[i] = 1

        return next_game



    def if_valid_move(self, move : tuple[int]) -> bool:     # type: ignore[override]
        if self.board[move[0]] <= 1:
            return True
        return False



    def get_possible_moves(self) -> tuple[tuple[int], ...]:
        valid_moves : list[tuple[int]] = []

        for i in range(self.size):
            if self.board[i] == 1:
                valid_moves.append( (i,) )

        return tuple(valid_moves)



    def get_winner(self) -> Side:
        tmp_board = c.copy(self.board)
        tmp_matrix = np.reshape(tmp_board, (3, 3))

        # Sorok és oszlopok ellenőrzése
        for i in range(3):
            row = tmp_matrix[i:i + 1]
            col = tmp_matrix[:, i:i + 1]

            if np.sum(row) == 14 or np.sum(col) == 14:
                return Side.FIRST
            elif np.sum(row) == 112 or np.sum(col) == 112:
                return Side.SECOND

        # Átlók ellenőrzése
        diag_main = np.diag(tmp_matrix)
        diag_sec = np.fliplr(tmp_matrix).diagonal()

        # o nyert
        if np.sum(diag_main) == 14 or np.sum(diag_sec) == 14:
            return Side.FIRST
        # x nyert
        elif np.sum(diag_main) == 112 or np.sum(diag_sec) == 112:
            return Side.SECOND

        # Senki sem nyert
        return Side.NONE



    def get_force_win(self) -> tuple[int]:
        tmp_board = np.zeros(self.size, dtype='int32')
        limit_min : int
        limit_max : int

        # Meglévő állás másolása a tmp_board-ba, úgy hogy a legöregebb jelet nem másoljuk,
        # mert miután teszünk egyet az úgyis eltűnik
        if self.side == Side.FIRST:
            limit_min = 6
            limit_max = 12
            for i in range(9):
                if self.board[i] != 8 and self.board[i] > 1:
                    tmp_board[i] = self.board[i]

        elif self.side == Side.SECOND:
            limit_min = 48
            limit_max = 96
            for i in range(9):
                if self.board[i] != 64 and self.board[i] > 1:
                    tmp_board[i] = self.board[i]

        tmp_matrix = np.reshape(tmp_board, (3, 3))

        # Sorok és oszlopok ellenőrzése
        for i in range(3):
            row = tmp_matrix[i:i + 1]
            col = tmp_matrix[:, i:i + 1]

            sum_row = np.sum(row)
            sum_col = np.sum(col)

            if sum_row >= limit_min and sum_row <= limit_max:
                for k in range(3):
                    if row[0][k] == 0 or row[0][k] == 1:
                        return (3 * i + k, )

            if sum_col >= limit_min and sum_col <= limit_max:
                for k in range(3):
                    if col[k][0] == 0 or col[k][0] == 1:
                        return (3 * k + i, )

        # Átlók ellenőrzése
        diag_main = np.diag(tmp_matrix)
        diag_sec = np.fliplr(tmp_matrix).diagonal()

        sum_diag_main = np.sum(diag_main)
        sum_diag_sec = np.sum(diag_sec)

        if sum_diag_main >= limit_min and sum_diag_main <= limit_max:
            for k in range(3):
                if diag_main[k] == 0 or diag_main[k] == 1:
                    return (4 * k, )

        if sum_diag_sec >= limit_min and sum_diag_sec <= limit_max:
            for k in range(3):
                if diag_sec[k] == 0 or diag_sec[k] == 1:
                    return (2 * k + 2, )

        return (-1, )



    def get_possible_last_positions(self) -> tuple[str, ...]:
        tmp_game = c.deepcopy(self)
        previous_side = (self.side + 1) % 2
        possible_last_positions : list[str] = []

        if previous_side == Side.FIRST:
            for i in range(self.size):
                if tmp_game.board[i] == 2:
                    tmp_game.board[i] = 1
                    last_move = i
                elif tmp_game.board[i] == 4 or tmp_game.board[i] == 8:
                    tmp_game.board[i] = int(tmp_game.board[i] / 2)

            for i in range(self.size):
                if tmp_game.board[i] == 1 and i != last_move:
                    tmp_game.board[i] = 8
                    tmp_game_transformed = tmp_game.decision_preparation()[0]
                    possible_last_positions.append(tmp_game_transformed.board2str())
                    tmp_game.board[i] = 1

        if previous_side == Side.SECOND:
            for i in range(self.size):
                if tmp_game.board[i] == 16:
                    tmp_game.board[i] = 1
                    last_move = i
                elif tmp_game.board[i] == 32 or tmp_game.board[i] == 64:
                    tmp_game.board[i] = int(tmp_game.board[i] / 2)
           
            for i in range(self.size):
                if tmp_game.board[i] == 1 and i != last_move:
                    tmp_game.board[i] = 64
                    tmp_game_transformed = tmp_game.decision_preparation()[0]
                    possible_last_positions.append(tmp_game_transformed.board2str())
                    tmp_game.board[i] = 1

        return tuple( possible_last_positions )
