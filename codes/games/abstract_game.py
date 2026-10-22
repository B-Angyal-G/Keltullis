import math as m
import numpy as np

from abc import ABC, abstractmethod
from numpy.typing import NDArray
from typing import Self

from games.abstract_game_display import abstract_game_display
from utils.side import Side




class abstract_game(abstract_game_display, ABC):
    size : int
    side : Side
    board: NDArray[np.int32]

    def __init__(self, side : int = 0) -> None:
        self.board = np.ones(self.size, dtype='int32')
        self.side = Side(side)

    def next_player(self) -> Side:
        return Side((self.side.value + 1) % 2)


    # <-- LÉPÉSEK -->
    # Lépés megtétele -> Új játékállás
    @abstractmethod
    def make_move(self, position : tuple[int, ...]) -> Self: ...

    @abstractmethod
    def if_valid_move(self, move : tuple[int, ...]) -> bool: ...

    # Győztes meghatározása
    # -1 : nincs győztes
    @abstractmethod
    def get_winner(self) -> int: ...

    # Győztes lépés meghatározása
    # Ha nincs, akkor -> return[0]-nak -1 -nek kell lennie!
    @abstractmethod
    def get_force_win(self) -> tuple[int, ...]: ...

    @abstractmethod
    def get_possible_moves(self) -> tuple[tuple[int, ...], ...]: ...



    # <-- JÁTÉK ELMENTÉSE/STRINGÉ ALAKÍTÁSA -->
    # Állás string-be kódolása
    @abstractmethod
    def board2str(self) -> str: ...

    # String-ből állás dekódolása
    @classmethod
    @abstractmethod
    def str2board(cls, str_board : str) -> Self: ...



    # <-- GÉP SZÁMÁRA JÁTÉKTÁBLA ÁTALAKÍTÁSA -->
    # Játéktábla transzformálása egyszerűsítéshez,
    # Bizonyos elemek kizárása szimmetria vagy tanulás útján
    # Nyerő lépéseket, egyértelmű védekező lépéseket itt kell beírni/felvenni a játék táblájára
    # int : kódolás kulcsa
    @abstractmethod
    def decision_preparation(self) -> tuple[Self, int]: ...

    # Transzformálás utáni eredmény dekódolása az eredeti táblára
    @abstractmethod
    def decision_decoder(self, inner_result : tuple[int, ...], tran : int) -> tuple[int, ...]: ...