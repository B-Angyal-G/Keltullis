from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.sign import Sign



class controller:
    game   : abstract_game
    player : abstract_player

    def __init__(self, game : abstract_game, player : abstract_player) -> None:
        self.game = game
        self.player = player

        
    def solve(self) -> tuple[int, ...]:
        transformed_game, tran = self.game.decision_preparation()
        inner_result = self.player.get_step(transformed_game)
        
        return self.game.decision_decoder(inner_result, tran)

        
