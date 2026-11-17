import numpy as np
import math as m
import copy as c
import random as r

from pathlib import Path

from games.abstract_game import abstract_game
from players.abstract_player import abstract_player




class mcts_simple_player(abstract_player):
    i  = 0

    def __init__(self, game_name : str) -> None:
        #                 game_string   total  win (simulation)
        self.experience_data : dict[ str, tuple[int, int] ] = self.load_experience( game_name )


    # MCTS lépése
    def get_move(self, game : abstract_game) -> tuple[int, ...]:
        # Ha van nyerő lépés, akkor azt lépjük
        FORCE_WIN = game.get_force_win()
        if FORCE_WIN[0] != -1:
            return FORCE_WIN

        # Összes lehetséges lépés meghatározása
        transformed_game, tran = game.decision_preparation()
        current_game_transformed_str = transformed_game.board2str()
        inner_possible_moves = transformed_game.get_possible_moves()

        possible_moves = []
        mcts_values = []
        for inner_move in inner_possible_moves:
            act_move = game.decision_decoder(inner_move, tran)
            possible_moves.append( act_move )
            mcts_val = self.mcts_eval( game.make_move(act_move),  current_game_transformed_str)
            mcts_values.append( mcts_val ) 

        # NEW
        # possible_moves_with_values = {}
        # for inner_move in inner_possible_moves:
        #     act_move = game.decision_decoder(inner_move, tran)
        #     mcts_val = self.mcts_eval( game.make_move(act_move),  current_game_transformed_str)
        #     possible_moves_with_values[act_move] = mcts_val

        # Max értéknek megfelelő lépéssel visszatérés
        # return max(possible_moves_with_values, key = possible_moves_with_values.get)
        return possible_moves[ np.argmax(mcts_values) ]




    def mcts_eval(self, game : abstract_game, last_position : str) -> float:
        # print(self.i)
        transformed_game = game.decision_preparation()[0]
        # self.i += 1
        game_board_str = transformed_game.board2str()

        if game_board_str in self.experience_data:
            # Adott csomópont látogatottsága és győzelmei
            n, w = self.experience_data[game_board_str]

            # Az adott csomópont (összes lehetséges) szülője látogatottsága
            # TODO: get_possible_last_positions() használata
            # possible_last_positions = game.get_possible_last_positions()
            # N = sum( self.experience_data[pos][0] for pos in possible_last_positions if pos in self.experience_data )

            if last_position in self.experience_data:
                N = self.experience_data[last_position][0]
            else:
                N = 1

            # MCTS értékelése c = sqrt(2) választással
            mcts_val = w/n + m.sqrt( 2 * m.log(N) / n )
            return mcts_val

        else:
            return 10000.0





   # MCTS adatkezelése 
    def get_file_path(self, game_name : str) -> Path:
        filename = game_name + "_mcts_data"
        
        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename
        
        return DATA


    def load_experience(self, game_name : str) -> dict[ str, list[int] ]:
        DATA = self.get_file_path(game_name)
    
        if DATA.is_file():
            read_data : dict[ str, list[int] ] = {}
            with open(DATA, "r", encoding="utf-8") as f:
                for line in f:
                    board_str = line[:-1]
                    xp = [ int(i) for i in f.readline().split(",") ]
                    read_data[board_str] = xp

            return read_data
        else:
            return {}


    def save_experience(self, game_name : str) -> None:
        DATA = self.get_file_path(game_name)
    
        with open(DATA, "w", encoding="utf-8") as f:
            f.write( "\n".join(f"{board_str}\n{str(xp[0]) + "," + str(xp[1])}" for board_str, xp in self.experience_data.items()) )





    # MCTS tanítása
    def simulation(self, game : abstract_game) -> tuple[ list[str], int ]:
        simulation_game = c.deepcopy(game)

        current_board_str : str
        history : list[str] = []

        self.i = 0
        while simulation_game.get_winner() == -1:
            self.i += 1
            print(self.i)
            # Lépés meghatározása
            move = self.get_move(simulation_game)

            # Lépés megtétele -> Side léptetése is
            simulation_game = simulation_game.make_move(move)

            # Állás elmentése
            transformed_game = simulation_game.decision_preparation()[0]
            current_board_str = transformed_game.board2str()

            history.append( current_board_str )

        return history, simulation_game.get_winner()



    def train(self, start_game : abstract_game, iteration : int = 1000) -> None:
        for i in range(1, iteration + 1):
            if i > 10:
                if i % (iteration // 10) == 0:
                    print(i)

            history, winner = self.simulation(start_game)

            # Adatok beírása experience_data-ba
            for i in range(len(history)):
                if history[i] not in self.experience_data:
                    self.experience_data[history[i]] = [0, 0]

                # Összes meccs száma
                self.experience_data[history[i]][0] += 1

                # Győztes
                if i % 2 == winner % 2:
                    self.experience_data[history[i]][1] += 1
            
        self.save_experience( type(start_game).__name__ )
