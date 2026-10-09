import numpy as np
import random

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game




class random_player(abstract_player):
    def get_step(self, game : abstract_game) -> tuple[int]:
        valid_positions = np.argwhere(game.board == 1)
        return (valid_positions[np.random.randint(len(valid_positions))][0], )
