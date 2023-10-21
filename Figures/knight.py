from Figures.figure import *


class Knight(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.possible_movements = ((1, 2), (-1, 2), (2, 1), (2, -1), (-1, -2), (1, -2), (-2, -1), (-2, 1))
        self.range = 1

    def get_icon(self):
        return '♘' if self.color is White else '♞'

    def copy(self):
        result = Knight(self.color)
        result.moves_count = self.moves_count
        return result

    def __str__(self):
        return "Knight"
