import os
import numpy as np

from dataclasses import dataclass
from pathlib import Path



# GAMES
from games.game_master import game_master
from games.infinite_tictactoe.infinite_tictactoe_game import infinite_tictactoe

# PLAYERS
from players.homo_sapiens_player import homo_sapiens_player
from players.minimax_player import minimax_player
from players.minimax_alphabeta_player import minimax_alphabeta_player
from players.mcts_player import mcts_player
from players.random_player import random_player

# UTILS
from utils.runtime import runtime
from utils.plot_matrix import plot_matrix



@dataclass
class training_data():
    file_name : str
    iteration : int
    param : float


def file2dataclass(file_name : str) -> training_data:
    file_name_parts = file_name.split('-')
    iteration = int( file_name_parts[2][1:] )
    param = float( file_name_parts[3][1:] )

    return training_data(file_name, iteration, param)




if __name__ == "__main__":
    PELDA = 0
    GAME  = 0
    TRAIN = 1
    BATTLE = 0

    if PELDA == 1:
        print("Minimax és Minimax alpha-beta vágás algoritmusok összehasonlítása:")
        player_minimax = minimax_player()
        player_minimax_alphabeta = minimax_alphabeta_player()

        game_string = "4032168020640"
        game = infinite_tictactoe.str2board(game_string)
        


        print('String-ből beolvasott állás:')
        game.print_tokens()
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



    if TRAIN == 1:
        game = infinite_tictactoe()
        player_mcts = mcts_player()
        
        # Tanítás folytatása egy file alapján
        # experience_name = 'mcts-infinite_tictactoe-i600-c1.41'
        # player_mcts.set_experience(experience_name)

        # player_mcts.train(game, 1000, 10)
        runtime(player_mcts.train, game, 2000, 10)


    if BATTLE == 1:
        PLAY = 1

        # === Adatok beolvasása === 
        ROOT = Path(__file__).parent
        DATA_FOLDER = ROOT.parent / "data"

        # MCTS-es file-ok kigyűjtése egy listába
        files = [f.name for f in DATA_FOLDER.iterdir() if f.is_file() and 'bak' not in f.name]

        # Dataclass-á alakítás
        for f in range(len(files)):
            files[f] = file2dataclass(files[f])

        # Rendezés paraméter értéke majd iterációs számok alapján
        files.sort(key=lambda f: (f.param, f.iteration))
        
        # Többdimenziós listává alakítás paraméter értéke szerint -> files_multidim
        i = 0
        files_multidim = []
        files_tmp = []
        while i < len(files):
            p = files[i].param
            while files[i].param == p:
                files_tmp.append(files[i])
                i += 1
                if i == len(files):
                    break
            files_multidim.append(files_tmp)
            files_tmp = []
            

        # === Egymás elleni meccsek lejátszása ===
        game = infinite_tictactoe()
        mcts_player1 = mcts_player(PLAY)
        mcts_player2 = mcts_player(PLAY)

        matrix_dim = len(files_multidim[0])
        result_matrix = np.zeros((matrix_dim, matrix_dim), dtype=float)
        for files_with_c in files_multidim: 
            for f1 in range(len(files_with_c)):
                experience_name1 = files_with_c[f1].file_name
                mcts_player1.set_experience(experience_name1)

                for f2 in range(len(files_with_c)):
                    experience_name2 = files_with_c[f2].file_name
                    mcts_player2.set_experience(experience_name2)

                    GM = game_master(mcts_player1, mcts_player2, game)
        
                    result = GM.play()

                    result_matrix[f1][f2] = result

        plot_matrix(result_matrix)
