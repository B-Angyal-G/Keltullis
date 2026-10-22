import copy as c

from pathlib import Path

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.side import Side




class ai_trainer:
    def __init__(self, player1 : abstract_player, player2 : abstract_player, game : abstract_game) -> None:
        self.players = player1, player2
        self.game = game
        self.experience_data : dict[ str, tuple[int, int] ] = {}


    def load_data(self) -> dict[ str, tuple[int, int] ]:
        filename = type(self.game).__name__
        filename += "_data"
        
        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename
        
        if DATA.is_file():
            read_data = {}
            with open(DATA, "r", encoding="utf-8") as f:
                board_str = f.readline()
                xp = [ int(i) for i in f.readline().split(",") ]
                read_data[board_str] = xp

            return read_data
        else:
            return {}



    def simulation(self) -> tuple[ list[str], int ]:
        self.players[0].init_data(self.experience_data)
        self.players[1].init_data(self.experience_data)

        current_player = self.players[0]
        inner_game = c.deepcopy(self.game)

        current_board_str : str
        history : list[str] = []

        while inner_game.get_winner() == -1:
            # Lépés meghatározása
            move = current_player.get_move(inner_game)

            # Lépés megtétele -> Side léptetése is
            inner_game = inner_game.make_move(move)

            # Állás elmentése
            current_board_str = inner_game.board2str()
            history.append( current_board_str )

            # Következő játékos
            current_player = self.players[ inner_game.side.value ]

        return history, inner_game.get_winner()



    def train(self, iteration : int = 1000) -> None:
        for _ in range(iteration):
            move_history, winner = self.simulation()

            print(move_history, winner)

            # Azokhoz az állásokhoz fogjuk írni a nyertest, ahova megérkezett a lépés után
            # Tehát azokban a másik játékos volt lépésen
            winner = (winner + 1) % 2

            # Adatok beírása experience_data-ba
            for pos in move_history:
                if pos in self.experience_data:
                    self.experience_data[pos][0] += 1
                    if int(pos[-1]) == winner:
                        self.experience_data[pos][1] += 1

                else:
                    if int(pos[-1]) == winner:
                        self.experience_data[pos] = [1, 1]
                    else:
                        self.experience_data[pos] = [1, 0]

        self.save_experience()



    def save_experience(self) -> None:
        filename = type(self.game).__name__
        filename += "_data"

        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename

        with open(DATA, "w", encoding="utf-8") as f:
            f.write( "\n".join(f"{board_str}\n{str(xp[0]) + "," + str(xp[1])}" for board_str, xp in self.experience_data.items()) )