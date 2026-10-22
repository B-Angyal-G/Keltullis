import numpy as np

from numpy.typing import NDArray
from typing import Self

from games.abstract_game import abstract_game
from utils.side import Side




class infinite_tictactoe_io(abstract_game):
    size : int
    side : Side
    board: NDArray[np.int32]


    def board2str(self) -> str:
        s = ""
        for element in self.board:
            if element > 1:
                s += str(element)
            else:
                s += '0'

        return s + str(self.side.value)



    @classmethod
    def str2board(cls, str_board : str) -> Self:
        read_game = cls( side = int(str_board[-1]) )
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