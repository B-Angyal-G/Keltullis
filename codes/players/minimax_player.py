import numpy as np
import random as r

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.sign import Sign




class minimax_player(abstract_player):
    def get_move(self, game : abstract_game) -> tuple[int, ...]:
        DEPTH = 12
        return self.minimax(game, DEPTH)[0]


    def minimax(self, game : abstract_game, DEPTH : int) -> tuple[tuple[int, ...], float]:  # [move, value]
        # Van-e nyerő lépés
        FORCE_WIN = game.get_force_win()
        if FORCE_WIN[0] != -1:
            if game.sign == Sign.CIRCLE:
                return FORCE_WIN, 1.0
            elif game.sign == Sign.CROSS:
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
                child_value = self.minimax(game.make_move(move), DEPTH - 1)[1]
                possible_moves[move] = child_value
                

            # Minimax választás
            if game.sign == Sign.CIRCLE:
                val = max(possible_moves.values())
                for k, v in possible_moves.items():
                    if v == val:
                        move = k
                        break
                return move, val

            elif game.sign == Sign.CROSS:
                val = min(possible_moves.values())
                for k, v in possible_moves.items():
                    if v == val:
                        move = k
                        break
                return move, val

        # Elértünk az előre kijelölt számítási mélységet
        # véletlenszerű értékkel visszatérünk
        return ((-1, ), r.uniform(-0.9, 0.9))
