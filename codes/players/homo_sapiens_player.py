import numpy as np
import math as m

from games.abstract_game import abstract_game
from players.abstract_player import abstract_player




class homo_sapiens_player(abstract_player):
    def load_values(self, game : abstract_game) -> None:
        pass


    def get_move(self, game : abstract_game) -> tuple[int]:
        game.print4play()

        # Beolvasandó értékek határai
        sq_size = int(m.sqrt(game.size))
        valid_set : set[int] = set(i for i in range(1, sq_size + 1))
        

        VALID = 0
        while VALID == 0:
            try:
                row = int(input("Row: "))
                col = int(input("Col: "))
            except:
                pass


            if row in valid_set and col in valid_set:
                move = ( 3 * (row - 1) + (col - 1), )
                if game.if_valid_move(move):
                    VALID = 1
                else:
                    print("\nInvalid move!")    
            else:
                print("\nInvalid input!")

        return move
