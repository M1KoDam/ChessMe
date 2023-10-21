from Figures.figure import *


class King(Figure):
    def __init__(self, color):
        super().__init__(color)
        self.possible_movements = ((1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1), (0, -4), (0, 3))
        self.castling = ((0, -4), (0, 3))
        self.range = 1

    def move(self):
        self.moves_count += 1

        if self.moves_count > 0:
            self.possible_movements = ((1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1))

    def move_back(self):
        self.moves_count -= 1
        if self.moves_count < 0:
            self.moves_count = 0

        if self.moves_count == 0:
            self.possible_movements = ((1, 1), (1, 0), (0, 1), (1, -1), (-1, 1), (-1, 0), (0, -1), (-1, -1), (0, -4), (0, 3))

    def get_icon(self):
        return '♔' if self.color is White else '♚'

    def copy(self):
        result = King(self.color)
        result.moves_count = self.moves_count
        return result

    def __str__(self):
        return "King"
