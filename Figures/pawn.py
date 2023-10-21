from Figures.figure import *


class Pawn(Figure):
    def __init__(self, color):
        super().__init__(color)
        if self.color is White:
            self.possible_movements = ((-1, 0), (-1, -1), (-1, 1))
            self.attacks = ((-1, -1), (-1, 1))
        else:
            self.possible_movements = ((1, 0), (1, -1), (1, 1))
            self.attacks = ((1, -1), (1, 1))
        self.range = 2

    def move(self):
        self.moves_count += 1

        if self.moves_count > 0:
            self.range = 1

    def move_back(self):
        self.moves_count -= 1
        if self.moves_count < 0:
            self.moves_count = 0

        if self.moves_count == 0:
            self.range = 2

    def get_icon(self):
        return '♙' if self.color is White else '♟'

    def copy(self):
        result = Pawn(self.color)
        result.possible_movements = self.possible_movements
        result.moves_count = self.moves_count
        return result

    def __str__(self):
        return "Pawn"
