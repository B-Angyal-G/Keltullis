from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.side import Side




class game_master:
    def __init__(self, player1 : abstract_player, player2 : abstract_player, game : abstract_game) -> None:
        self.players = player1, player2
        self.game = game


    def play(self) -> float:
        current_player = self.players[0]

        i = 0
        while self.game.get_winner() == -1:
            i += 1
            # Döntetlen
            if i == 100:
                return 0.5

            # Lépés meghatározása
            move = current_player.get_move(self.game)

            # Lépés megtétele -> Side lép
            self.game = self.game.make_move(move)

            # Következő játékos
            current_player = self.players[ self.game.side.value ]

        # self.game.print4play()
        # print(f"Nyertes: { Side( self.game.get_winner() ).name }!")
        return self.game.get_winner().value
