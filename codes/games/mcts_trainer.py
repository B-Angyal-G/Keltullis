import copy as c

from pathlib import Path

from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.side import Side




class mcts_trainer:
    def __init__(self, player1 : abstract_player, player2 : abstract_player, game : abstract_game) -> None:
        self.players = player1, player2
        self.game = game
        self.experience_data = self.load_data()


    def load_data(self) -> dict[ str, tuple[int, int] ]:
        filename = type(self.game).__name__
        filename += "_mcts_data"
        
        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename
    
        if DATA.is_file():
            read_data = {}
            with open(DATA, "r", encoding="utf-8") as f:
                for line in f:
                    board_str = line[:-1]
                    xp = [ int(i) for i in f.readline().split(",") ]
                    read_data[board_str] = xp

            return read_data
        else:
            return {}



    def simulation(self) -> tuple[ list[str], int ]:
        self.players[0].init_data(self.experience_data)
        self.players[1].init_data(self.experience_data)

        current_player = self.players[0]
        simulation_game = c.deepcopy(self.game)

        current_board_str : str
        history : list[str] = []

        while simulation_game.get_winner() == -1:
            # Lépés meghatározása
            move = current_player.get_move(simulation_game)

            # Lépés megtétele -> Side léptetése is
            simulation_game = simulation_game.make_move(move)

            # Állás elmentése
            current_board_str = simulation_game.board2str()
            history.append( current_board_str )

            # Következő játékos
            current_player = self.players[ simulation_game.side.value ]

        return history, simulation_game.get_winner()



    def train(self, iteration : int = 1000) -> None:
        for i in range(1, iteration + 1):
            if i % 1000 == 0:
                print(i)

            history, winner = self.simulation()

            # Adatok beírása experience_data-ba
            for i in range(len(history)):
                if history[i] not in self.experience_data:
                    self.experience_data[history[i]] = [0, 0]

                # Összes meccs száma
                self.experience_data[history[i]][0] += 1

                # Győztes
                if i % 2 == winner.value % 2:
                    self.experience_data[history[i]][1] += 1
            
        self.save_experience()



    def save_experience(self) -> None:
        filename = type(self.game).__name__
        filename += "_mcts_data"
        
        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename
    
        with open(DATA, "w", encoding="utf-8") as f:
            f.write( "\n".join(f"{board_str}\n{str(xp[0]) + "," + str(xp[1])}" for board_str, xp in self.experience_data.items()) )
