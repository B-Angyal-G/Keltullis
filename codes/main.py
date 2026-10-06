import numpy as np


from abstract_game import Sign

from infinite_tictactoe_game import infinite_tictactoe

from random_player import random_player
from minimax_player import minimax_player




if __name__ == "__main__":
    player_minimax = minimax_player() 
    game_string = "4163264002801"
    game = infinite_tictactoe.str2board(game_string)

    print('String-ből beolvasott állás:')
    game.print_signs()
    print()
    
    move = player_minimax.get_step(game)

    print('Minimax algoritmus lépése:', move)
