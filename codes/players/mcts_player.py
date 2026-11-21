import numpy as np
import math as m
import copy as c
import random as r

from pathlib import Path

from games.abstract_game import abstract_game
from players.abstract_player import abstract_player



class mcts_player(abstract_player):

    def __init__(self, play : int = 0) -> None:
        #                        game_string   total / win (simulation)
        self.experience_data : dict[ str, list[float] ] = {}
        self.c : float = m.sqrt(2)
        self.iter_num = int = 0
        self.PLAY = play


    # Példányváltozók beállítása
    def set_experience(self, file_name : str) -> None:
        self.iter_num = int( file_name.split('-')[2][1:]   )    # file nevéből adódó iterációs szám
        self.c        = float( file_name.split('-')[3][1:] )    # file nevéből adódó paraméter érték
        self.experience_data = self.load_experience(file_name)


    def set_c(self, c : float) -> None:
        self.c = c


    def hard_reset(self):
        self.experience_data = {}
        self.iter_num = 0


   # MCTS adatkezelése 
    def get_file_path(self, file_name : str) -> Path:
        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / file_name
        
        return DATA


    def load_experience(self, file_name : str) -> dict[ str, list[float] ]:
        DATA = self.get_file_path(file_name)
    
        if DATA.is_file():
            read_data : dict[ str, list[float] ] = {}
            with open(DATA, "r", encoding="utf-8") as f:
                for line in f:
                    board_str = line[:-1]
                    xp = [ float(i) for i in f.readline().split(",") ]
                    read_data[board_str] = xp

            return read_data
        else:
            return {}


    def save_experience(self, file_name : str) -> None:
        DATA = self.get_file_path(file_name)
    
        with open(DATA, "w", encoding="utf-8") as f:
            f.write( "\n".join(f"{board_str}\n{str(xp[0]) + "," + str(xp[1])}" for board_str, xp in self.experience_data.items()) )





    # MCTS lépése
    def get_move(self, game : abstract_game, PLAY : int = 0) -> tuple[int, ...]:
        # Ha van nyerő lépés, akkor azt lépjük
        FORCE_WIN = game.get_force_win()
        if FORCE_WIN[0] != -1:
            return FORCE_WIN

        # Összes lehetséges lépés meghatározása
        # TODO: Végiggondolni, hogy transzformációkat lehet-e csökkenteni
        transformed_game, tran = game.decision_preparation()
        current_game_transformed_str = transformed_game.board2str()
        inner_possible_moves = transformed_game.get_possible_moves()

        possible_moves = []
        mcts_values = []
        for inner_move in inner_possible_moves:
            act_move = game.decision_decoder(inner_move, tran)
            possible_moves.append( act_move )
            mcts_val = self.mcts_eval( game.make_move(act_move),  current_game_transformed_str )
            mcts_values.append( mcts_val ) 

        # Max értéknek megfelelő lépéssel visszatérés
        return possible_moves[ self.random_argmax(mcts_values) ]


    def random_argmax(self, values):
        max_value = max(values)
        indices = [i for i in range(len(values)) if values[i] == max_value]
        return r.choice(indices)


    def mcts_eval(self, game : abstract_game, last_position : str) -> float:
        transformed_game = game.decision_preparation()[0]
        game_board_str = transformed_game.board2str()

        if game_board_str in self.experience_data:
            # Adott csomópont látogatottsága és győzelmei
            n, w = self.experience_data[game_board_str]

            if self.PLAY == 1:
                # TODO: n és w alapján jobb választási logika írása
                return self.choose4play(n, w)

            # Az adott csomópont (összes lehetséges) szülőjének látogatottsága
            possible_last_positions = game.get_possible_last_positions()
            N = sum( self.experience_data[pos][0] for pos in possible_last_positions if pos in self.experience_data )
            if N == 0:
                N = 1

            # MCTS értékelése
            mcts_val = w/n + self.c * m.sqrt( m.log(N) / n )
            return mcts_val

        else:
            return 10000.0



    def choose4play(self, n : float, w : float) -> float:
        return n



    # MCTS tanítása
    def simulation(self, game : abstract_game) -> tuple[ list[str], int ]:
        simulation_game = c.deepcopy(game)

        current_board_str : str
        history : list[str] = []

        i = 0
        while simulation_game.get_winner() == -1:
            i += 1
            # Döntetlen 50 lépés után
            if i == 50:
                return history, -1


            # Lépés meghatározása
            move = self.get_move(simulation_game)

            # Lépés megtétele -> Side léptetése is
            simulation_game = simulation_game.make_move(move)

            # Állás elmentése
            transformed_game = simulation_game.decision_preparation()[0]
            current_board_str = transformed_game.board2str()

            history.append( current_board_str )

        return history, simulation_game.get_winner()



    def train(self, start_game : abstract_game, iteration : int = 1000, frac : int = 10) -> None:
        game_name = type(start_game).__name__
        iteration_limit = iteration + self.iter_num
        while self.iter_num < iteration_limit:
            self.iter_num += 1

            history, winner = self.simulation(start_game)

            # Adatok beírása experience_data-ba
            for i in range(len(history)):
                if history[i] not in self.experience_data:
                    self.experience_data[history[i]] = [0, 0]

                # Összes meccs száma
                self.experience_data[history[i]][0] += 1

                # Győztes vagy döntetlen
                if winner != -1:
                    if i % 2 == winner % 2:
                        self.experience_data[history[i]][1] += 1
                else:
                    self.experience_data[history[i]][1] += 0.5

            if self.iter_num >= frac:
                if self.iter_num % (iteration // frac) == 0:
                    file_name = 'mcts-' + game_name + '-i' + str(self.iter_num) + '-c' + str(self.c)[0:4]
                    self.save_experience( file_name )
                    print(self.iter_num,'-> saved: ' + file_name)
