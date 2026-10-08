import math as m
import numpy as np

from abc import ABC, abstractmethod
from numpy.typing import NDArray

from displays.abstract_game_display import abstract_game_display
from utils.sign import Sign




class abstract_game(abstract_game_display, ABC):
    size: int
    sign: Sign
    board: NDArray[np.int32]

    def __init__(self, sign: int = 0) -> None:
        self.board = np.ones(self.size, dtype='int32')
        self.sign = Sign(sign)

    def next_player(self) -> Sign:
        return Sign((self.sign.value + 1) % 2)

    # Lépés megtétele -> Új játékállás
    @abstractmethod
    def make_step(self, position: int) -> "abstract_game": ...

    # Állás string-be kódolása
    @abstractmethod
    def board2str(self) -> str: ...

    # String-ből állás dekódolása
    @classmethod
    @abstractmethod
    def str2board(str_board: str) -> "abstract_game": ...

    # Győztes meghatározása
    @abstractmethod
    def get_winner(self) -> int: ...

    # Győztes lépés meghatározása
    @abstractmethod
    def get_force_win(self) -> int: ...

    # Játéktábla transzformálása egyszerűsítéshez,
    # Bizonyos elemek kizárása szimmetria vagy tanulás útján
    @abstractmethod
    def decision_preparation(self) -> tuple["abstract_game", int]: ...

    # Transzformálás utáni eredmény dekódolása az eredeti táblára
    @abstractmethod
    def decision_decoder(self) -> int: ...
