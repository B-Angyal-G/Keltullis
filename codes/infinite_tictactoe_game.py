import numpy as np
import math as m
import copy as c

from abstract_game import abstract_game, Sign
from infinite_tictactoe_game_display import infinite_tictactoe_display



class infinite_tictactoe(abstract_game, infinite_tictactoe_display):
    size = 9
    
    def make_step(self, position: int) -> "infinite_tictactoe":
        next_sign = self.next_player()
        next_game = infinite_tictactoe(sign = next_sign)
        next_game.board = c.copy(self.board)

        # Kör: 2, 4, 8
        if self.sign == Sign.CIRCLE:
            for i in range(9):
                if i == position:
                    next_game.board[i] = 2
                elif self.board[i] == 2 or self.board[i] == 4:
                    next_game.board[i] *= 2
                elif self.board[i] == 8 or self.board[i] == 0:
                    next_game.board[i] = 1

        # X: 16, 32, 64
        if self.sign == Sign.CROSS:
            for i in range(9):
                if i == position:
                    next_game.board[i] = 16
                elif self.board[i] == 16 or self.board[i] == 32:
                    next_game.board[i] *= 2
                elif self.board[i] == 64 or self.board[i] == 0:
                    next_game.board[i] = 1
                    
        return next_game


    def board2str(self) -> str:
        s = ""
        for element in self.board:
            if element > 1:
                s += str(element)
            else:
                s += '0'

        return s + str(self.sign.value)


    @classmethod
    def str2board(cls, str_board : str) -> "infinite_tictactoe":
        read_game = infinite_tictactoe(sign = int(str_board[-1]))
        s = 0
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
        tmp_board = c.copy(self.board)
        tmp_matrix = np.reshape(tmp_board, (3, 3))

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
            return 1
        # x nyert
        elif np.sum(diag_main) == 112 or np.sum(diag_sec) == 112:
            return -1

        # Senki sem nyert
        return 0


    def get_force_win(self) -> int:
        tmp_board = np.zeros(self.size, dtype='int32')
        
        # Meglévő állás másolása a tmp_board-ba, úgy hogy a legöregebb jelet nem másoljuk,
        # mert miután teszünk egyet az eltűnik 
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
                        return 3 * i + k

            if sum_col >= limit_min and sum_col <= limit_max:
                for k in range(3):
                    if col[k][0] == 0 or col[k][0] == 1:
                        return 3 * k + i

        # Átlók ellenőrzése
        diag_main = np.diag(tmp_matrix)
        diag_sec = np.fliplr(tmp_matrix).diagonal()

        sum_diag_main = np.sum(diag_main)
        sum_diag_sec = np.sum(diag_sec)

        if sum_diag_main >= limit_min and sum_diag_main <= limit_max:
            for k in range(3):
                if diag_main[k] == 0 or diag_main[k] == 1:
                    return 4 * k

        if sum_diag_sec >= limit_min and sum_diag_sec <= limit_max:
            for k in range(3):
                if diag_sec[k] == 0 or diag_sec[k] == 1:
                    return 2 * k + 2

        return -1


    def decision_preparation(self) -> "infinite_tictactoe":
        pass
