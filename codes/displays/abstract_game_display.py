import math as m
import numpy as np

from abc import ABC, abstractmethod
from numpy.typing import NDArray

from utils.sign import Sign




class abstract_game_display(ABC):
    size : int
    sign : Sign
    board : NDArray[np.int32]

    def __str__(self) -> str:
        s = "Board:\n"
        sq = int(m.sqrt(self.size))
        for row in self.board.reshape((sq, sq)):
            for element in row:
                s = s + str(element) + " "
            s += "\n"

        s = s + "Sign: " + str(self.sign.value)

        return s


    def print_board(self) -> None:
        # TODO: Kirajzolás szépítése, táblás játékszerűsítése
        sq = int( m.sqrt(self.size) )
        for row in self.board.reshape((sq, sq)):
            for element in row:
                print(element, end=' ')
            print()



    @abstractmethod
    def print_signs(self) -> None: ...

    @abstractmethod
    def print4play(self) -> None: ...
