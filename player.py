from Figures.figure import Figure
from encode_decode import *


def handle_input(text):
    """Обработка пользовательского ввода"""
    while True:
        guess = input(text).replace(' ', '')
        try:
            spl = list(guess)

            if not (spl[0] in letter_transcription.keys() and spl[1] in number_transcription.keys() or
                    spl[1] in letter_transcription.keys() and spl[0] in number_transcription.keys()):
                print("Incorrect input!")
                continue

            if spl[0] in letter_transcription.keys():
                cell = (number_transcription[spl[1]], letter_transcription[spl[0]])
            else:
                cell = (number_transcription[spl[0]], letter_transcription[spl[1]])

            return cell
        except:
            print("Incorrect input!")


class Player:
    def __init__(self, color):
        self.color = color

    def try_do_step(self, chessboard):
        # Выбор фигуры
        cell = handle_input(f">>> {self.color.color}, choose your figure: ")
        figure = chessboard.square[cell[0]][cell[1]]
        if figure is None:
            print("You can't choose empty cell!")
            return False
        if self.color != figure.color:
            print("It's not your turn!")
            return False
        if not issubclass(figure.__class__, Figure):
            print("Incorrect input!")
            return False

        # Выбор клетки
        target_cell = handle_input(">>> Choose your target cell: ")

        # Ход
        return cell, target_cell

    def __str__(self):
        return f"class Player"
