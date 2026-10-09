# GAMES
from games.game_master import game_master
from games.infinite_tictactoe_game import infinite_tictactoe

# PLAYERS
from players.homo_sapiens_player import homo_sapiens_player
from players.minimax_player import minimax_player
from players.minimax_alphabeta_player import minimax_alphabeta_player
from players.random_player import random_player
from players.controller import controller

from utils.runtime import runtime



if __name__ == "__main__":
    PELDA : int = 0
    GAME  : int = 1

    if PELDA == 1:
        print("Minimax és Minimax alpha-beta vágás algoritmusok összehasonlítása:")
        player_minimax : abstract_player = minimax_player()
        player_minimax_alphabeta : abstract_player = minimax_alphabeta_player()

        game_string = "4032168020640"
        game : abstract_game = infinite_tictactoe.str2board(game_string)


        minimax_controller : controller = controller(game, player_minimax)
        minimax_alphabeta_controller : controller = controller(game, player_minimax_alphabeta)


        print('String-ből beolvasott állás:')
        game.print_signs()
        print()

        step = runtime(player_minimax.get_step, game)[0]
        print('Minimax algoritmus lépése:', step[0])

        print()
        step = runtime(player_minimax_alphabeta.get_step, game)[0]
        print('Minimax alpha-beta vágás algoritmus lépése:', step[0])
        print("\n\n")


    if GAME == 1:
        # Inicializálások
        player_minimax           : abstract_player = minimax_player()
        player_minimax_alphabeta : abstract_player = minimax_alphabeta_player()
        player_homo_sapiens      : abstract_player = homo_sapiens_player()

        game : abstract_game = infinite_tictactoe()

        minimax_controller : controller = controller(game, player_minimax)
        minimax_alphabeta_controller : controller = controller(game, player_minimax_alphabeta)

        game_master : game_master = game_master(player_homo_sapiens, player_minimax_alphabeta, game)


        game_master.play()
