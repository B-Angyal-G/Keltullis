import numpy as np
import math as m

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game




class homo_sapiens_player(abstract_player):
    def get_step(self, game : abstract_game) -> int:
        game.print4play()

        # Beolvasandó értékek határai
        sq = int(m.sqrt(game.size))
        valid_set = set(i for i in range(1, sq + 1))

        
        VALID = 0
        while VALID == 0:
            row = int(input("Row: "))
            col = int(input("Col: "))

            if {row, col} in valid_set:
                step = 3 * (row - 1) + (col - 1)
                VALID = 1
            else:
                print("\nInvalid input!")

        return step
