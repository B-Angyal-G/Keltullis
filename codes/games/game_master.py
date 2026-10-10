from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.sign import Sign



class game_master:
    def __init__(self, player1 : abstract_player, player2 : abstract_player, game : abstract_game) -> None:
        self.players = player1, player2
        self.game = game

    def play(self) -> None:
        current_player : abstract_player = self.players[0]

        while self.game.get_winner() == -1:
            # Lépés meghatározása
            step = current_player.get_step(self.game)

            # Lépés megtétele -> Sign lép
            self.game = self.game.make_step(step)

            # Következő játékos
            current_player = self.players[ self.game.sign.value ]


        self.game.print4play()
        print(f"Nyertes: { Sign( self.game.get_winner() ).name }!")
