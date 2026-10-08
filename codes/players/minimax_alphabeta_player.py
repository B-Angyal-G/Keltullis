import numpy as np
import random as r

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game, Sign


class minimax_alphabeta_player(abstract_player):
    def get_step(self, game: abstract_game) -> int:
        DEPTH: int = 12
        alpha: int = -2
        beta:  int = 2
        return self.minimax_alphabeta(game, alpha, beta, DEPTH)[0]

    def minimax_alphabeta(self, game: abstract_game, alpha: int, beta: int, DEPTH: int) -> tuple[int, float]:  # [step, value]
        # Van-e nyerő lépés
        FORCE_WIN = game.get_force_win()
        if FORCE_WIN != -1:
            if game.sign == Sign.CIRCLE:
                return FORCE_WIN, 1
            elif game.sign == Sign.CROSS:
                return FORCE_WIN, -1

        while DEPTH != 0:
            # Megvizsgálandó ágak felvétele -> possible_steps
            # 0-val lesz inicializálva
            possible_steps: dict[int, float] = dict()

            for element in range(game.size):
                if game.board[element] == 1:
                    possible_steps[element] = 0

            # Lehetséges lépésekhez értékek hozzárendelése
            # TODO: FORBIDDEN_POS HASZNÁLATA
            for step in possible_steps:
                child_value = self.minimax_alphabeta(game.make_step(step), alpha, beta, DEPTH - 1)[1]
                possible_steps[step] = child_value

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
                val = max(possible_steps.values())
                for k, v in possible_steps.items():
                    if v == val:
                        step = k
                        break
                return step, val

            elif game.sign == Sign.CROSS:
                val = min(possible_steps.values())
                for k, v in possible_steps.items():
                    if v == val:
                        step = k
                        break
                return step, val

        # Elértünk az előre kijelölt számítási mélységet
        # véletlenszerű értékkel visszatérünk
        return [-1, r.uniform(-0.9, 0.9)]
