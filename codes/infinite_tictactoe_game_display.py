import math as m

from abstract_game_display import abstract_game_display



class infinite_tictactoe_display(abstract_game_display):
    def print_signs(self) -> None:
        s = "Táblázat:\n"
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
