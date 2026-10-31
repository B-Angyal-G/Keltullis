import copy as c

from pathlib import Path

from trainers.abstract_trainer import abstract_trainer
from players.abstract_player import abstract_player
from games.abstract_game import abstract_game

from utils.side import Side




class mcts_trainer(abstract_trainer):
    def load_data(self) -> dict[ str, list[int] ]:
        DATA = self.get_file_path()
    
        if DATA.is_file():
            read_data : dict[ str, list[int] ] = {}
            with open(DATA, "r", encoding="utf-8") as f:
                for line in f:
                    board_str = line[:-1]
                    xp = [ int(i) for i in f.readline().split(",") ]
                    read_data[board_str] = xp

            return read_data
        else:
            return {}



    def simulation(self) -> tuple[ list[str], int ]:
        self.player.init_data(self.experience_data)

        simulation_game = c.deepcopy(self.game)

        current_board_str : str
        history : list[str] = []

        while simulation_game.get_winner() == -1:
            # Lépés meghatározása
            move = self.player.get_move(simulation_game)

            # Lépés megtétele -> Side léptetése is
            simulation_game = simulation_game.make_move(move)

            # Állás elmentése
            transformed_game = simulation_game.decision_preparation()[0]
            current_board_str = transformed_game.board2str()

            history.append( current_board_str )

        return history, simulation_game.get_winner()



    def train(self, iteration : int = 1000) -> None:
        for i in range(1, iteration + 1):
            if i % (iteration // 10) == 0:
                print(i)

            history, winner = self.simulation()

            # Adatok beírása experience_data-ba
            for i in range(len(history)):
                if history[i] not in self.experience_data:
                    self.experience_data[history[i]] = [0, 0]

                # Összes meccs száma
                self.experience_data[history[i]][0] += 1

                # Győztes
                if i % 2 == winner % 2:
                    self.experience_data[history[i]][1] += 1
            
        self.save_experience()



    def save_experience(self) -> None:
        DATA = self.get_file_path()
    
        with open(DATA, "w", encoding="utf-8") as f:
            f.write( "\n".join(f"{board_str}\n{str(xp[0]) + "," + str(xp[1])}" for board_str, xp in self.experience_data.items()) )
