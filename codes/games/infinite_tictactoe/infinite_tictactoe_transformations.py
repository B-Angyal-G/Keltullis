import numpy as np
import copy as c

from numpy.typing import NDArray
from typing import Self

from games.abstract_game import abstract_game
from games.infinite_tictactoe.tictactoe_transformations import transformations
from utils.side import Side




class infinite_tictactoe_transformations(abstract_game):
    size : int
    side : Side
    board: NDArray[np.int32]


    # Egységes álláshoz szükséges transzformáció megkeresése
    def find_transformation(self) -> int:
        tmp_board = c.copy(self.board)
        tmp_matrix = np.reshape(tmp_board, (3, 3))

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

        return -1


    
    # Tábla forgatása egységes állásra, transzformáció visszaadása is
    def transform_board(self) -> tuple[NDArray[np.int32], int]:
        tmp_board = c.copy(self.board)
        t = self.find_transformation()

        if t == -1:
            raise ValueError("Cannot find the proper transformation!")

        return np.dot(tmp_board, transformations[t]), t



    def mask_symmetric(self) -> None:
        board_refl_vert = np.dot(self.board, transformations[4])
        board_refl_diag = np.dot(self.board, transformations[7])

        VERT_SYMMETRY = 0
        DIAG_SYMMETRY = 0


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



    def decision_preparation(self) -> tuple[Self, int]:
        transformed_game = type(self)()
        transformed_board, tran = self.transform_board()

        transformed_game.board = c.copy(transformed_board)
        transformed_game.mask_symmetric()
        transformed_game.side = self.side

        return transformed_game, tran



    def decision_decoder(self, inner_result : tuple[int], tran : int) -> tuple[int]:    # type: ignore[override]
        # result[0]-nak megfelelő oszlopban levő 1-es helye
        return ( int( np.argmax(transformations[tran][:, inner_result[0]:inner_result[0] + 1]) ), )