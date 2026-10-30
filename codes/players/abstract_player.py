from abc import ABC, abstractmethod
from games.abstract_game import abstract_game



class abstract_player(ABC):
    @abstractmethod
    def get_move(self, game : abstract_game) -> tuple[int, ...]: ...

    @abstractmethod
    def init_data(self, experience_data : dict[ str, tuple[int, int] ]) -> None: ...
