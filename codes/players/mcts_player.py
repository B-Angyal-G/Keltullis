import numpy as np
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
        #                 game_string        move              total  win (simulation)
        self.data_map : dict[ str, tuple[tuple[int, ...], tuple[int, float]] ] = {}


    def load_values(self, game : abstract_game) -> None:
        filename = self.get_filename(game)

        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename

        if DATA.is_file():
            print("Loading in progress...")

    

    def get_move(self, game : abstract_game) -> tuple[int, ...]:
        # game.print_board()
        DEPTH = 12
        alpha = -2.0
        beta = 2.0
        
        result = self.minimax_alphabeta(game, alpha, beta, DEPTH, mcts_eval, max, min)
        # if result[1] == 1 or result[1] == -1:
        #     # Ha a visszatérési érték +/- 1, akkor egyértelmű nyerést talált.
        #     print('Van nyerő stratégiám!')
            
        return result[0]



    # TODO
    def mcts_eval(self, game : abstract_game) -> float:
        pass



    def init_data(self, experience_data : dict[ str, tuple[int, int] ]) -> None:
        pass