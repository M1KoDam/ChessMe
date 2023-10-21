from Figures.figure import *


class Queen(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.possible_movements = ((1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1))
        self.range = 8

    def get_icon(self):
        return '♕' if self.color is White else '♛'

    def copy(self):
        result = Queen(self.color)
        result.moves_count = self.moves_count
        return result

    def __str__(self):
        return "Queen"
