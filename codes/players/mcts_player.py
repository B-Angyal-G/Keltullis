import numpy as np
import math as m
import copy as c
import random as r

from collections.abc import Callable, Iterable
from pathlib import Path

from games.abstract_game import abstract_game
from players.abstract_player import abstract_player
from players.minimax_alphabeta_player import minimax_alphabeta
from utils.side import Side




class mcts_player(abstract_player):
    # def minimax_alphabeta(self, game : abstract_game, alpha : float, beta : float, DEPTH : int,
    #                       eval_func : Callable[[abstract_game], float], max_choose : Callable[[Iterable[float]], float], min_choose : Callable[[Iterable[float]], float]) -> tuple[tuple[int, ...], float]:  # [move, value]
    
    def __init__(self) -> None:
        #                 game_string   total  win (simulation)
        self.data_map : dict[ str, tuple[int, float] ] = {}


    def load_values(self, game : abstract_game) -> None:
        filename = self.get_filename(game)

        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename

        if DATA.is_file():
            print("Loading in progress...")

    

    def get_move(self, game : abstract_game) -> tuple[int, ...]:
        # game.print_board()
        DEPTH = 3   # PÁRATLANNAK KELL LENNIE!
        alpha = -20000.0
        beta = 20000.0
        
        result = minimax_alphabeta(game, alpha, beta, DEPTH, self.mcts_eval, self.max_choose, self.min_choose)
        # if result[1] == 1 or result[1] == -1:
        #     # Ha a visszatérési érték +/- 1, akkor egyértelmű nyerést talált.
        #     print('Van nyerő stratégiám!')
            
        return result[0]






    def mcts_eval(self, game : abstract_game) -> float:
        # print('INNER DATA_MAP:', self.data_map)
        game_board_str = game.board2str

        if game_board_str in self.data_map:
            # Adott csomópont látogatottsága és győzelmei
            n, w = self.data_map[game_board_str]

            # Az adott csomópont (összes lehetséges) szülője látogatottsága
            possible_last_positions = game.get_possible_last_positions()
            N = sum( self.data_map[pos][0] for pos in possible_last_positions )

            # MCTS értékelése c = sqrt(2) választással
            mcts_val = w/n + m.sqrt( 2 * m.log(N) / n )
            print(mcts_val)
            print('ITT:', mcts_val / 10)
            return mcts_val / 10

        else:
            return 10000.0



    def max_choose(self, values : tuple[float]) -> float:
        tmp_vals = list(values)
        for i in range(len(tmp_vals)):
            if m.isclose(tmp_vals[i], 1.0):
                return 1.0
            elif m.isclose(tmp_vals[i], -1.0):
                tmp_vals[i] = 0.000000001


        print(tmp_vals)
        return r.choices(tmp_vals, weights = tmp_vals, k = 1)[0]
        


    def min_choose(self, values : tuple[float]) -> float:
        tmp_vals = list(values)
        for i in range(len(tmp_vals)):
            if m.isclose(tmp_vals[i], -1.0):
                return -1.0

        return r.choices(tmp_vals, weights = tmp_vals, k = 1)[0]



    def init_data(self, experience_data : dict[ str, tuple[int, int] ]) -> None:
        self.data_map = c.deepcopy(experience_data)
