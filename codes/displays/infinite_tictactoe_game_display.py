import math as m

from displays.abstract_game_display import abstract_game_display




class infinite_tictactoe_display(abstract_game_display):
    def print_signs(self) -> None:
        s = "Board:\n"
        sq = int(m.sqrt(self.size))
        for row in self.board.reshape((sq, sq)):
            for element in row:
                if element <= 8 and element > 1:
                    s = s + "o" + " "
                elif element > 8:
                    s = s + "x" + " "
                else:
                    s = s + "." + " "
            s += "\n"

        s = s + "Sign: " + str(self.sign.value)
        print(s)



    def print4play(self) -> None:
        s = "\n\n"
        sq = int(m.sqrt(self.size))
        tmp_board = self.board.reshape((sq, sq))
        
        # Felso sor
        print("   ", end="")
        for i in range(sq):
            print(i + 1, end=" ")
        print()

        print("   ", end="")
        for i in range(sq):
            print("_", end=" ")
        print()

        # Táblázat
        for row in range(sq):
            # Első oszlop
            print(row + 1, end="| ")

            for col in range(sq):
                if tmp_board[row][col] <= 8 and tmp_board[row][col] > 1:
                    print("o", end=" ")
                elif tmp_board[row][col] > 8:
                    print("x", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()
