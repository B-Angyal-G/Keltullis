import numpy as np
import random as r

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.sign import Sign




class minimax_player(abstract_player):
    def get_step(self, game : abstract_game) -> tuple[int]:
        DEPTH : int = 12
        return self.minimax(game, DEPTH)[0]


    def minimax(self, game : abstract_game, DEPTH : int) -> tuple[tuple[int], float]:  # [step, value]
        # Van-e nyerő lépés
        FORCE_WIN : tuple[int] = game.get_force_win()
        if FORCE_WIN[0] != -1:
            if game.sign == Sign.CIRCLE:
                return FORCE_WIN, 1
            elif game.sign == Sign.CROSS:
                return FORCE_WIN, -1

        while DEPTH != 0:
            # Megvizsgálandó ágak felvétele -> possible_steps
            # 0-val lesz inicializálva
            possible_steps : dict[tuple[int], float] = dict()

            for position in range(game.size):
                if game.board[position] == 1:
                    possible_steps[(position, )] = 0

            # Lehetséges lépésekhez értékek hozzárendelése
            for step in possible_steps:
                child_value = self.minimax(game.make_step(step), DEPTH - 1)[1]
                possible_steps[step] = child_value
                

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
        return [(-1, ), r.uniform(-0.9, 0.9)]
