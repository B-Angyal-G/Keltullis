import numpy as np

from numpy.typing import NDArray


from games.infinite_tictactoe.infinite_tictactoe_basic import infinite_tictactoe_basic
from games.infinite_tictactoe.infinite_tictactoe_io import infinite_tictactoe_io
from games.infinite_tictactoe.infinite_tictactoe_transformations import infinite_tictactoe_transformations
from games.infinite_tictactoe.infinite_tictactoe_display import infinite_tictactoe_display

from utils.side import Side




# Egységesítő osztály
class infinite_tictactoe(infinite_tictactoe_basic, infinite_tictactoe_io, infinite_tictactoe_transformations, infinite_tictactoe_display):
    size = 9
    side : Side
    board: NDArray[np.int32]
