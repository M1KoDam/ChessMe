from imports import *
from Enums.steps import *
from encode_decode import *


class Chessboard:
    def __init__(self, square=None):
        self.square = square
        if square is None:
            self.square = [
                [Rook(Black), Knight(Black), Bishop(Black), Queen(Black), King(Black), Bishop(Black), Knight(Black),
                 Rook(Black)],
                [Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black)],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White)],
                [Rook(White), Knight(White), Bishop(White), Queen(White), King(White), Bishop(White), Knight(White),
                 Rook(White)]
            ]

        self.movements = []
        self.desks = []
        self.dead_white = []
        self.dead_black = []
        self.steps_to_draw = [0]

        self.dead_figures = {White: self.dead_white, Black: self.dead_black}
        self.moves_count = lambda: len(self.movements)

    def add_movement(self, movement):
        if isinstance(movement.cur_figure, Pawn) or issubclass(movement.step_type, Attack):
            self.steps_to_draw.append(0)
        else:
            self.steps_to_draw.append(self.steps_to_draw[-1]+1)

        if issubclass(movement.step_type, Attack):
            self.dead_figures[movement.target_figure.color].append(movement.target_figure)

        self.desks.append(encode_chessboard(self))
        self.movements.append(movement)

    def delete_movement(self, movement):
        if issubclass(movement.step_type, Attack):
            self.dead_figures[movement.target_figure.color].pop()

        self.steps_to_draw.pop()
        self.desks.pop()
        self.movements.pop()

    def __str__(self):
        numbers = [1, 2, 3, 4, 5, 6, 7, 8]
        board = "   a  b  c d  e  f g  h\n"
        for raw in self.square:
            board += f"{numbers.pop()} |"
            for cell in raw:
                board += f"{'、' if cell is None else cell.get_icon()}|"
            board += "\n"
        return board[:-1]

    def print_desk(self):
        self.__str__()

    def print_dead(self, color):
        result = ""
        for figure in self.dead_white if color is White else self.dead_black:
            result += f"{figure.get_icon()} "
        return result[:-1]

    def render_desk(self):
        """Отрисовка"""
        result = self.print_dead(White) + '\n' + self.__str__() + '\n' + self.print_dead(Black)
        print(result)
        return result

    def clear(self):
        self.__init__()

    def copy(self):
        new_chessboard = Chessboard()
        for w in range(8):
            for h in range(8):
                cur_cell = (w, h)
                cur_figure = self.square[cur_cell[0]][cur_cell[1]]
                new_chessboard.square[cur_cell[0]][cur_cell[1]] = None if cur_figure is None else cur_figure.copy()

        for figure in self.dead_black:
            new_chessboard.dead_black.append(figure.copy())

        for figure in self.dead_white:
            new_chessboard.dead_white.append(figure.copy())

        new_chessboard.moves_count = self.moves_count
        return new_chessboard


def main():
    pass


if __name__ == "__main__":
    main()
