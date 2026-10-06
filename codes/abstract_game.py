import math as m
import numpy as np

from abc import ABC, abstractmethod
from enum import IntEnum



class Sign(IntEnum):
    CIRCLE = 0
    CROSS = 1



class abstract_game(ABC):
    size : int

    def __init__(self, sign : int = 0) -> None:
        self.board = np.ones(self.size, dtype='int32')
        self.sign = Sign(sign)


    def __str__(self):
        s = "Táblázat:\n"
        sq = int(m.sqrt(self.size))
        for row in self.board.reshape((sq, sq)):
            for element in row:
                s = s + str(element) + " "
            s += "\n"

        s = s + "Sign: " + str(self.sign.value)
        return s

    def print_all(self) -> None:
        # TODO: Kirajzolás szépítése, táblás játékszerűsítése
        sq = int( m.sqrt(self.size) )
        for row in self.board.reshape((sq, sq)):
            for element in row:
                print(element, end=' ')
            print()

    def next_player(self) -> Sign:
        return Sign( (self.sign.value + 1) % 2 )

    @abstractmethod
    def print_signs(self) -> None: ...

    @abstractmethod
    def make_step(self, position : int) -> "abstract_game": ...


    @abstractmethod
    def board2str(self) -> str: ...

    @classmethod
    @abstractmethod
    def str2board(str_board : str) -> "abstract_game": ...


    @abstractmethod
    def get_winner(self) -> int: ...
    
    @abstractmethod
    def get_force_win(self) -> int: ...
    
    # TODO: Felhasználni
    @abstractmethod
    def decision_preparation(self) -> "abstract_game": ...
