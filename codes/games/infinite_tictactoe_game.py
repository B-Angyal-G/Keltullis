import numpy as np
import math as m
import copy as c

from games.abstract_game import abstract_game
from numpy.typing import NDArray

from utils.tictactoe_transformations import *
from utils.sign import Sign

from displays.infinite_tictactoe_game_display import infinite_tictactoe_display




class infinite_tictactoe(abstract_game, infinite_tictactoe_display):
    size : int = 9

    def make_step(self, position : tuple[int]) -> "infinite_tictactoe":
        next_game : abstract_game = infinite_tictactoe( sign = self.next_player() )
        next_game.board = c.copy(self.board)

        # Kör: 2, 4, 8
        if self.sign == Sign.CIRCLE:
            for i in range(9):
                if i == position[0]:
                    next_game.board[i] = 2
                elif self.board[i] == 2 or self.board[i] == 4:
                    next_game.board[i] *= 2
                elif self.board[i] == 8 or self.board[i] == 0:
                    next_game.board[i] = 1

        # X: 16, 32, 64
        if self.sign == Sign.CROSS:
            for i in range(9):
                if i == position[0]:
                    next_game.board[i] = 16
                elif self.board[i] == 16 or self.board[i] == 32:
                    next_game.board[i] *= 2
                elif self.board[i] == 64 or self.board[i] == 0:
                    next_game.board[i] = 1

        return next_game



    def board2str(self) -> str:
        s : str = ""
        for element in self.board:
            if element > 1:
                s += str(element)
            else:
                s += '0'

        return s + str(self.sign.value)



    @classmethod
    def str2board(cls, str_board : str) -> "infinite_tictactoe":
        read_game : abstract_game = infinite_tictactoe(sign=int(str_board[-1]))
        s : int = 0
        for i in range(read_game.size):
            if str_board[s] in {'2', '4', '8'}:
                read_game.board[i] = int(str_board[s])
            elif str_board[s] == '1':
                read_game.board[i] = 16
                s += 1
            elif str_board[s] == '3':
                read_game.board[i] = 32
                s += 1
            elif str_board[s] == '6':
                read_game.board[i] = 64
                s += 1
            s += 1

        return read_game



    def get_winner(self) -> int:
        tmp_board : NDArray = c.copy(self.board)
        tmp_matrix : NDArray = np.reshape(tmp_board, (3, 3))

        # Sorok és oszlopok ellenőrzése
        for i in range(3):
            row = tmp_matrix[i:i + 1]
            col = tmp_matrix[:, i:i + 1]

            if np.sum(row) == 14 or np.sum(col) == 14:
                return 0
            elif np.sum(row) == 112 or np.sum(col) == 112:
                return 1

        # Átlók ellenőrzése
        diag_main = np.diag(tmp_matrix)
        diag_sec = np.fliplr(tmp_matrix).diagonal()

        # o nyert
        if np.sum(diag_main) == 14 or np.sum(diag_sec) == 14:
            return 0
        # x nyert
        elif np.sum(diag_main) == 112 or np.sum(diag_sec) == 112:
            return 1

        # Senki sem nyert
        return -1



    def get_force_win(self) -> tuple[int]:
        tmp_board : NDArray = np.zeros(self.size, dtype='int32')
        limit_min : int
        limit_max : int

        # Meglévő állás másolása a tmp_board-ba, úgy hogy a legöregebb jelet nem másoljuk,
        # mert miután teszünk egyet az úgyis eltűnik
        if self.sign == Sign.CIRCLE:
            limit_min = 6
            limit_max = 12
            for i in range(9):
                if self.board[i] != 8 and self.board[i] > 1:
                    tmp_board[i] = self.board[i]

        elif self.sign == Sign.CROSS:
            limit_min = 48
            limit_max = 96
            for i in range(9):
                if self.board[i] != 64 and self.board[i] > 1:
                    tmp_board[i] = self.board[i]

        tmp_matrix : NDArray = np.reshape(tmp_board, (3, 3))

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



    # Egységes álláshoz szükséges transzformáció megkeresése
    def find_transformation(self) -> int:
        tmp_board : NDArray = c.copy(self.board)
        tmp_matrix : NDArray = np.reshape(tmp_board, (3, 3))

        # 2x3-as részek összege
        board_forms6_sum = np.array(
            [np.sum(tmp_matrix[:2]),
             np.sum(tmp_matrix[:, 1:3]),
             np.sum(tmp_matrix[1:3]),
             np.sum(tmp_matrix[:, :2])],
            dtype='int32'
        )

        # 2x2-es sarkok összege
        board_forms4_sum = np.array(
            [np.sum(tmp_matrix[:2][:, :2]),
             np.sum(tmp_matrix[:2][:, 1:]),
             np.sum(tmp_matrix[1:][:, 1:]),
             np.sum(tmp_matrix[1:][:, :2])],
            dtype='int32'
        )

        # 2x3-asok maximum elemeinek indexei
        idx_max6 = np.flatnonzero(board_forms6_sum == board_forms6_sum.max())
        index_max6 = idx_max6[0]

        # Ha csak egy max 2x3-as rész van
        if idx_max6.size == 1:
            if board_forms4_sum[index_max6] > board_forms4_sum[(index_max6 + 1) % 4]:
                return index_max6
            else:
                return index_max6 + 4

        else:
            index_max4 = np.argmax(board_forms4_sum)

            match index_max4:
                case 0:
                    if self.board[1] >= self.board[3]:
                        return 0
                    return 7
                case 1:
                    if self.board[5] >= self.board[1]:
                        return 1
                    return 4
                case 2:
                    if self.board[7] >= self.board[5]:
                        return 2
                    return 5
                case 3:
                    if self.board[3] >= self.board[7]:
                        return 3
                    return 6


    
    # Tábla forgatása egységes állásra, transzformáció visszaadása is
    def transform_board(self) -> tuple[NDArray[int], int]:
        tmp_board : NDArray = c.copy(self.board)
        t : int = self.find_transformation()

        return np.dot(tmp_board, transformations[t]), t



    def mask_symmetric(self) -> None:
        board_refl_vert : NDArray = np.dot(self.board, transformations[4])
        board_refl_diag : NDArray = np.dot(self.board, transformations[7])

        VERT_SYMMETRY : int = 0
        DIAG_SYMMETRY : int = 0


        if np.array_equal(self.board, board_refl_vert):
            VERT_SYMMETRY = 1
        if np.array_equal(self.board, board_refl_diag):
            DIAG_SYMMETRY = 1

        if VERT_SYMMETRY == 1:
            for i in range(3):
                if self.board[2 + 3 * i] == 1:
                    self.board[2 + 3 * i] = 0

        if DIAG_SYMMETRY == 1:
            if self.board[3] == 1:
                self.board[3] = 0
            if self.board[6] == 1:
                self.board[6] = 0
            if self.board[7] == 1:
                self.board[7] = 0



    def decision_preparation(self) -> tuple["infinite_tictactoe", int]:
        transformed_game : abstract_game = infinite_tictactoe()
        transformed_board, tran = self.transform_board()

        transformed_game.board = c.copy(transformed_board)
        transformed_game.mask_symmetric()
        transformed_game.sign = self.sign

        return transformed_game, tran



    def decision_decoder(self, inner_result : tuple[int], tran : int) -> tuple[int]:
        return ( np.argmax(transformations[tran][:, inner_result[0]:inner_result[0] + 1]), )    # result[0]-nak megfelelő oszlopban levő 1-es helye
