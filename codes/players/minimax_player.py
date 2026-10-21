import numpy as np
import random as r

from collections.abc import Callable, Iterable

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game
from utils.side import Side




class minimax_player(abstract_player):
    def load_values(self, game : abstract_game) -> None:
        pass



    def get_move(self, game : abstract_game) -> tuple[int, ...]:
        DEPTH = 12
        return self.minimax(game, DEPTH, self.minimax_random_eval, max, min)[0]


    def minimax(self, game : abstract_game, DEPTH : int,
                eval_func : Callable[[abstract_game], float], max_choose : Callable[[Iterable[float]], float], min_choose : Callable[[Iterable[float]], float]) -> tuple[tuple[int, ...], float]:  # [move, value]
        # Van-e nyerő lépés
        FORCE_WIN = game.get_force_win()
        if FORCE_WIN[0] != -1:
            if game.side == Side.FIRST:
                return FORCE_WIN, 1.0
            elif game.side == Side.SECOND:
                return FORCE_WIN, -1.0

        while DEPTH != 0:
            # Megvizsgálandó ágak felvétele -> possible_moves
            # {lépés : érték} párok, 0-val inicializálva
            # TODO: FORBIDDEN_POS HASZNÁLATA
            possible_moves : dict[tuple[int, ...], float] = dict()

            transformed_game, tran = game.decision_preparation()
            inner_possible_moves = transformed_game.get_possible_moves()

            for inner_move in inner_possible_moves:
                decoded_move = game.decision_decoder(inner_move, tran)
                possible_moves[decoded_move] = 0.0

            # Lehetséges lépésekhez értékek hozzárendelése
            for move in possible_moves:
                child_value = self.minimax(game.make_move(move), DEPTH - 1, eval_func, max, min)[1]
                possible_moves[move] = child_value
                

            # Minimax választás
            if game.side == Side.FIRST:
                val = max_choose(possible_moves.values())
                for k, v in possible_moves.items():
                    if v == val:
                        move = k
                        break
                return move, val

            elif game.side == Side.SECOND:
                val = min_choose(possible_moves.values())
                for k, v in possible_moves.items():
                    if v == val:
                        move = k
                        break
                return move, val

        # Elértünk az előre kijelölt számítási mélységet
        # véletlenszerű értékkel visszatérünk
        value = eval_func(game)
        return ((-1, ), value)



    def minimax_random_eval(self, game : abstract_game) -> float:
        return r.uniform(-0.9, 0.9)
