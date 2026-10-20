# GAMES
from games.game_master import game_master
from games.infinite_tictactoe_game import infinite_tictactoe

# PLAYERS
from players.homo_sapiens_player import homo_sapiens_player
from players.minimax_player import minimax_player
from players.minimax_alphabeta_player import minimax_alphabeta_player
from players.random_player import random_player

from utils.runtime import runtime



if __name__ == "__main__":
    PELDA = 1
    GAME  = 1

    if PELDA == 1:
        print("Minimax és Minimax alpha-beta vágás algoritmusok összehasonlítása:")
        player_minimax = minimax_player()
        player_minimax_alphabeta = minimax_alphabeta_player()

        game_string = "4032168020640"
        game = infinite_tictactoe.str2board(game_string)
        


        print('String-ből beolvasott állás:')
        game.print_signs()
        print()

        move = runtime(player_minimax.get_move, game)[0]
        print('Minimax algoritmus lépése:', move[0])

        print()
        move = runtime(player_minimax_alphabeta.get_move, game)[0]
        print('Minimax alpha-beta vágás algoritmus lépése:', move[0])
        print("\n\n")


    if GAME == 1:
        # Inicializálások
        player_minimax           = minimax_player()
        player_minimax_alphabeta = minimax_alphabeta_player()
        player_homo_sapiens      = homo_sapiens_player()

        game = infinite_tictactoe()

        GM = game_master(player_homo_sapiens, player_minimax_alphabeta, game)

        GM.play()
