from board import abstract_board

class tictac_board(abstract_board):
    def print_sign(self) -> None:
        print("*")

    def board2str(self, sign : int = None) -> str:
        return "*"

    # Megfelelő jel elhelyezése
    def place_sign(self, position : int, sign : int) -> None:
        print("Placed")
