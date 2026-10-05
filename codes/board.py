from abc import ABC, abstractmethod

import math as m
import numpy as np



class abstract_board(ABC):
    def __init__(self, TileCount : int) -> None:
        self._array = np.ones(TileCount, dtype='int32')

    @property
    def array(self) -> NDArray[np.integer]:
        return self._array

    def __len__(self) -> int:
        return len(self._array)

    def __getitem__(self, index : int) -> np.integer:
        return self._array[index]

    def __setitem__(self, index : int, value : int) -> None:
        self._array[index] = value


    # <--- Absztrakt függvények, amik játéktól függnek --->
    # Játéktábla jelekkel történő kiíratása
    @abstractmethod
    def print_sign(self) -> None: ...

    @abstractmethod
    def board2str(self, sign : int = None) -> str: ...


    # Mentett string-ből tábla visszaállítása
    # ÁTGONDOLNI, HOGY EGY STRING AZ NEM BOARD OBJEKTUM
    # @abstractmethod
    # def str2board(self, str_board : str) -> NDArray[np.integer]: ...


    # Megfelelő jel elhelyezése
    @abstractmethod
    def place_sign(self, position : int, sign : int) -> None: ...



    # <--- Saját függvények--->
    def print(self):
        width = int(m.sqrt(len(self)))

        print("   ", end='')
        for i in range(1, width + 1):
            print(i, end=' ')
        print()

        print("   ", end='')
        for i in range(1, width + 1):
            print('_', end=' ')
        print()
        
        board_matrix = np.reshape(self._array, (width, width))
        for i in range(1, width + 1):
            print(i, end='| ')
            for j in board_matrix[i - 1]:
                print(j, end=' ')
            print()
        print()
