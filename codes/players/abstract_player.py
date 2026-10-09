from abc import ABC, abstractmethod
from games.abstract_game import abstract_game



class abstract_player(ABC):
    @abstractmethod
    def get_step(self, game : abstract_game) -> tuple[int, ...]: ...
