import numpy as np
import random as r

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.sign import Sign



class minimax_alphabeta_player(abstract_player):
    def get_move(self, game : abstract_game) -> tuple[int, ...]:
        # game.print_board()
        DEPTH = 12
        alpha = -2.0
        beta = 2.0
        
        result = self.minimax_alphabeta(game, alpha, beta, DEPTH)
        # if result[1] == 1 or result[1] == -1:
        #     # Ha a visszatérési érték +/- 1, akkor egyértelmű nyerést talált.
        #     print('Van nyerő stratégiám!')
            
        return result[0]

    def minimax_alphabeta(self, game : abstract_game, alpha : float, beta : float, DEPTH : int) -> tuple[tuple[int, ...], float]:  # [move, value]
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
                child_value = self.minimax_alphabeta(game.make_move(move), alpha, beta, DEPTH - 1)[1]
                possible_moves[move] = child_value

                # Alpha - Beta vágás
                if game.sign == Sign.CIRCLE:
                    alpha = max(alpha, child_value)
                    if beta <= alpha:
                        break
                        
                elif game.sign == Sign.CROSS:
                    beta = min(beta, child_value)
                    if alpha >= beta:
                        break


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
        # TODO: MCTS, Q-Learning
        return ((-1, ), r.uniform(-0.9, 0.9))
