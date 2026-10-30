from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.side import Side




class game_master:
    def __init__(self, player1 : abstract_player, player2 : abstract_player, game : abstract_game) -> None:
        self.players = player1, player2
        self.game = game


    def play(self) -> None:
        # TODO: LOAD_DATA
        current_player = self.players[0]

        while self.game.get_winner() == -1:
            # Lépés meghatározása
            move = current_player.get_move(self.game)

            # Lépés megtétele -> Side lép
            self.game = self.game.make_move(move)

            # Következő játékos
            current_player = self.players[ self.game.side.value ]


        self.game.print4play()
        print(f"Nyertes: { Side( self.game.get_winner() ).name }!")
