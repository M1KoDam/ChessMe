from chess_func import *
import random


class ChessAI:
    def __init__(self, color):
        self.color = color

    def try_do_step(self, chessboard):
        print("Thinking... Please Wait")

        moves = []
        for w in range(8):
            for h in range(8):
                cur_cell = (w, h)
                cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
                if not (issubclass(cur_figure.__class__, Figure) and cur_figure.color == self.color):
                    continue

                for possible_movement in cur_figure.possible_movements:
                    for r in range(1, cur_figure.range + 1):
                        step_cell = (cur_cell[0] + possible_movement[0] * r, cur_cell[1] + possible_movement[1] * r)
                        if step_cell[0] < 0 or step_cell[0] > 7 or step_cell[1] < 0 or step_cell[1] > 7:
                            break

                        movement = do_step(chessboard, cur_cell, step_cell, out_info=False, pawn_auto_upgrade=True)
                        if not movement:
                            continue

                        rollback_step(chessboard, movement)
                        moves.append((cur_cell, step_cell))

        return random.choice(moves)

    def __str__(self):
        return f"class STUPID_AI(By STPD_Ai_CLUB)"


if __name__ == "main":
    pass
