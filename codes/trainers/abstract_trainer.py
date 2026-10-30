from abc import ABC, abstractmethod
from typing import Any
from pathlib import Path

from games.abstract_game import abstract_game
from players.abstract_player import abstract_player



class abstract_trainer(ABC):
    def __init__(self, player : abstract_player, game : abstract_game) -> None:
        self.player = player
        self.game = game
        self.experience_data = self.load_data()


    def get_file_path(self) -> Path:
        game_name = type(self.game).__name__
        player_name = type(self.player).__name__
        player_name = player_name.split("_")[0]     # Levágjuk a player részt

        filename = game_name + "_" + player_name + "_data"
        
        ROOT = Path(__file__).parent
        DATA = ROOT.parent.parent / "data" / filename
        
        return DATA



    @abstractmethod
    def load_data(self) -> dict[ Any, Any ]: ...

    @abstractmethod
    def save_experience(self) -> None: ...

    @abstractmethod
    def train(self, iteration : int) -> None: ...
