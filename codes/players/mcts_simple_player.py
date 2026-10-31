import numpy as np
import math as m
import copy as c
import random as r

from pathlib import Path

from games.abstract_game import abstract_game
from players.abstract_player import abstract_player




class mcts_simple_player(abstract_player):
    def __init__(self) -> None:
        #                 game_string   total  win (simulation)
        self.data_map : dict[ str, tuple[int, int] ] = {}


    def init_data(self, experience_data : dict[ str, tuple[int, int] ]) -> None:
        self.data_map = c.deepcopy(experience_data)
    



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
            possible_moves.append( game.decision_decoder(inner_move, tran) )
            test_val = self.mcts_eval( game.make_move(possible_moves[-1]),  current_game_transformed_str)
            mcts_values.append( test_val ) 

        # Súlyozott választás
        if set(mcts_values) == {0}:
            mcts_values = [1] * len(mcts_values)
        choosen_move = r.choices(possible_moves, weights = mcts_values, k = 1)[0]

        return choosen_move




    def mcts_eval(self, game : abstract_game, last_position : str) -> float:
        transformed_game = game.decision_preparation()[0]
        game_board_str = transformed_game.board2str()

        if game_board_str in self.data_map:
            # Adott csomópont látogatottsága és győzelmei
            n, w = self.data_map[game_board_str]

            # Az adott csomópont (összes lehetséges) szülője látogatottsága
            # TODO: get_possible_last_positions() használata
            # possible_last_positions = game.get_possible_last_positions()
            # N = sum( self.data_map[pos][0] for pos in possible_last_positions if pos in self.data_map )

            if last_position in self.data_map:
                N = self.data_map[last_position][0]
            else:
                N = 1

            # MCTS értékelése c = sqrt(2) választással
            mcts_val = w/n + m.sqrt( 2 * m.log(N) / n )
            return mcts_val

        else:
            return 10000.0
