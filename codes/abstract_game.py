import math as m
import numpy as np

from abc import ABC, abstractmethod
from enum import IntEnum

from abstract_game_display import abstract_game_display



class Sign(IntEnum):
    CIRCLE = 0
    CROSS = 1



class abstract_game(abstract_game_display, ABC):
    size : int
    sign : Sign
    board : NDArray[int32]


    def __init__(self, sign : int = 0) -> None:
        self.board = np.ones(self.size, dtype='int32')
        self.sign = Sign(sign)



    def next_player(self) -> Sign:
        return Sign( (self.sign.value + 1) % 2 )



    # Lépés megtétele -> Új játékállás
    @abstractmethod
    def make_step(self, position : int) -> "abstract_game": ...


    # Állás string-be kódolása
    @abstractmethod
    def board2str(self) -> str: ...

    # String-ből állás dekódolása
    @classmethod
    @abstractmethod
    def str2board(str_board : str) -> "abstract_game": ...


    # Győztes meghatározása
    @abstractmethod
    def get_winner(self) -> int: ...
    
    # Győztes lépés meghatározása
    @abstractmethod
    def get_force_win(self) -> int: ...
    
    # Játéktábla egységes helyzetre transzformálása
    # TODO: Felhasználni
    @abstractmethod
    def decision_preparation(self) -> "abstract_game": ...
