from abc import ABC, abstractmethod
from games.abstract_game import abstract_game



class abstract_player(ABC):
    def get_filename(self, game : abstract_game) -> str:
        filename = type(self).__name__
        filename = filename.replace("player", type(game).__name__)
        filename += "_data"

        return filename


    @abstractmethod
    def load_values(self, game : abstract_game) -> None: ...

    @abstractmethod
    def get_move(self, game : abstract_game) -> tuple[int, ...]: ...
