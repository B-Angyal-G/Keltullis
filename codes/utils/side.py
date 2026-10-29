from enum import IntEnum

class Side(IntEnum):
    FIRST = 0
    SECOND = 1
    NONE = -1

    def next_player(self) -> Side:
        return Side.FIRST if self == Side.SECOND else Side.SECOND
