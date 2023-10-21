import unittest
from chess_func import *
from ChessAi import *
# coverage для тестирования на питоне чтобы проверить покрытие тестами


class ChessFuncTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ChessFuncTest, self).__init__(*args, **kwargs)
        self.chessboard = Chessboard([
            [Rook(Black), None, None, None, King(Black), Bishop(Black), Knight(Black), Rook(Black)],
            [Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), Pawn(Black), None, Pawn(Black)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White), Pawn(White)],
            [Rook(White), Knight(White), Bishop(White), Queen(White), King(White), None, None, Rook(White)]]
        )
        do_step(self.chessboard, (6, 4), (4, 4))
        do_step(self.chessboard, (1, 3), (3, 3))
        do_step(self.chessboard, (4, 4), (3, 4))
        do_step(self.chessboard, (1, 1), (2, 1))
        do_step(self.chessboard, (6, 2), (4, 2))
        print(self.chessboard)

    def test_pawn_attack(self):
        self.assertIsNotNone(do_step(self.chessboard, (3, 3), (4, 2)))
        print(self.chessboard)

    def test_pawn_en_passant(self):
        do_step(self.chessboard, (1, 5), (3, 5))
        self.assertIsNotNone(do_step(self.chessboard, (3, 4), (2, 5)))
        print(self.chessboard)

    def test_pawn_cant_move_2_squares_forward(self):
        self.assertIsNone(do_step(self.chessboard, (2, 1), (4, 1)))
        print(self.chessboard)

    def test_pawn_can_move_2_squares_forward(self):
        self.assertIsNotNone(do_step(self.chessboard, (6, 0), (4, 0)))
        print(self.chessboard)

    def test_cant_do_castling(self):
        do_step(self.chessboard, (7, 3), (4, 6))
        self.assertIsNone(do_step(self.chessboard, (0, 4), (0, 7)))
        self.assertIsNone(do_step(self.chessboard, (0, 4), (0, 0)))
        print(self.chessboard)

    def test_can_do_castling(self):
        self.assertIsNotNone(do_step(self.chessboard, (0, 4), (0, 0)))
        self.assertIsNotNone(do_step(self.chessboard, (7, 4), (7, 7)))
        print(self.chessboard)


class EventTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(EventTest, self).__init__(*args, **kwargs)
        self.white_Ai = ChessAI(White)
        self.black_Ai = ChessAI(Black)

        self.chessboard = Chessboard([
            [King(Black), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, King(White), None, None, None, None],
            [None, None, None, Pawn(White), None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        )

    def test_check_by_three_same_desk_positions(self):
        for i in range(3):
            do_step(self.chessboard, (0, 0), (0, 1))
            do_step(self.chessboard, (3, 3), (3, 2))
            do_step(self.chessboard, (0, 1), (0, 0))
            do_step(self.chessboard, (3, 2), (3, 3))
        self.assertEqual(is_draw(self.chessboard, White), True)
        print(self.chessboard)

    def test_check_by_50_steps(self):
        step = (0, 0)
        sign = 1
        for count in range(4):
            for i in range(7):
                new_step = (step[0], step[1]+sign)
                do_step(self.chessboard, step, new_step)
                step = new_step
                print(self.chessboard)
            for i in range(7):
                new_step = (step[0]+sign, step[1])
                do_step(self.chessboard, step, new_step)
                step = new_step
                print(self.chessboard)
            sign *= -1

        print(self.chessboard.steps_to_draw[-1])
        self.assertEqual(is_draw(self.chessboard, Black), True)
        print(self.chessboard)

    def test_check_by_no_steps(self):
        chessboard = Chessboard([
            [King(Black), None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(White), King(White), None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]]
        )

        do_step(chessboard, (2, 0), (1, 0))
        self.assertEqual(is_draw(chessboard, Black), True)
        print(chessboard)


class ChessAITest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(ChessAITest, self).__init__(*args, **kwargs)
        self.white_Ai = ChessAI(White)
        self.black_Ai = ChessAI(Black)

        self.chessboard = Chessboard([
            [None, None, None, None, King(Black), None, None, None],
            [None, None, None, None, Queen(Black), None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn(White), Pawn(White), Pawn(White), None, None, None, None, None],
            [None, King(White), None, None, None, None, None, None]]
        )

    def test_black_can_checkmate_in_one_step(self):
        movement_cell = self.black_Ai.try_do_step(self.chessboard)
        print(do_step(self.chessboard, movement_cell[0], movement_cell[1]))
        self.assertEqual(is_checkmate(self.chessboard, White), True)
        print(self.chessboard)

    def test_white_can_ecape_checkmate(self):
        movement_cell = self.white_Ai.try_do_step(self.chessboard)
        print(do_step(self.chessboard, movement_cell[0], movement_cell[1]))
        movement_cell = self.black_Ai.try_do_step(self.chessboard)
        print(do_step(self.chessboard, movement_cell[0], movement_cell[1]))
        self.assertEqual(is_checkmate(self.chessboard, White), False)
        print(self.chessboard)


if __name__ == '__main__':
    unittest.main()
