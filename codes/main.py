# GAMES
from games.infinite_tictactoe_game import infinite_tictactoe

# PLAYERS
from players.minimax_player import minimax_player
from players.minimax_alphabeta_player import minimax_alphabeta_player
from players.random_player import random_player
from players.controller import controller

from utils.runtime import runtime


if __name__ == "__main__":
    player_minimax = minimax_player()
    player_minimax_alphabeta = minimax_alphabeta_player()

    game_string = "4032168020640"
    game = infinite_tictactoe.str2board(game_string)


    game.print4play()
    print()
    print('col')
    print('row')
    exit()
    minimax_alphabeta_controller = controller(game, player_minimax_alphabeta)
    result = runtime(minimax_alphabeta_controller.solve)
    print('Kontroller eredmény:', result)

    print('String-ből beolvasott állás:')
    game.print_signs()
    print()

    move = runtime(player_minimax.get_step, game)[0]
    print('Minimax algoritmus lépése:', move)

    print()
    move = runtime(player_minimax_alphabeta.get_step, game)[0]
    print('Minimax alpha-beta vágás algoritmus lépése:', move)
