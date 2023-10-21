from chess_func import *
from AI_positions import *
from Enums.difficulties import *


class ChessAI:
    def __init__(self, color, difficulty=EASY, info_output=False):
        self.color = color
        self.difficulty = difficulty
        self.figure_cost = {None: 0, Pawn: 1, Rook: 5, Bishop: 3, Knight: 3, Queen: 9}
        self.info_output = info_output

        self.figure_kill_weight = 10
        self.figure_loose_weight = 10
        self.self_pos_weight = 1
        self.enemy_pos_weight = 1
        if difficulty is EASY:
            self.deep = 3
        else:
            self.deep = 5

    def try_do_step(self, chessboard):
        print("Thinking... Please Wait")
        ai_step = self.do_ai_step(chessboard, self.color, 0)[0]
        return ai_step

    def do_ai_step(self, chessboard, color, cur_deep, prev_score=0, lim_prev_score=-1000):
        if cur_deep >= self.deep:
            return None, 0, []

        lim_cur_score = -1000 if color is self.color else 1000
        lim_cur_steps = None
        lim_cur_log = []
        lim_cur_log_score = lim_cur_score

        for w in range(8):
            for h in range(8):
                cur_cell = (w, h) if color is White else (7 - w, 7 - h)
                cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
                if not (issubclass(cur_figure.__class__, Figure) and cur_figure.color == color):
                    continue

                for possible_movement in cur_figure.possible_movements:
                    for r in range(1, cur_figure.range + 1):
                        step_cell = (cur_cell[0] + possible_movement[0] * r, cur_cell[1] + possible_movement[1] * r)
                        if step_cell[0] < 0 or step_cell[0] > 7 or step_cell[1] < 0 or step_cell[1] > 7:
                            break
                        step_figure = chessboard.square[step_cell[0]][step_cell[1]]

                        if isinstance(step_figure, King):
                            break

                        cur_steps = (cur_cell, step_cell)
                        cur_score = 0
                        cur_log = []
                        movement = do_step(chessboard, cur_cell, step_cell, out_info=False, pawn_auto_upgrade=True)

                        if not movement:
                            continue

                        if is_chessboard_draw(chessboard):
                            rollback_step(chessboard, movement)
                            continue

                        if is_check(chessboard, get_other_color(color)):
                            cur_score += 5 if color is self.color else -5

                        atk_score = self.figure_cost[movement.target_figure_class]
                        if movement.step_type is Castling:
                            atk_score = 0
                        pos_score = AIPos.choose_color[color][cur_figure.__class__][step_cell[0]][step_cell[1]]

                        if color is self.color:
                            cur_score += self.figure_kill_weight * atk_score + self.self_pos_weight * pos_score
                        elif color is not self.color:
                            cur_score -= self.figure_loose_weight * atk_score + self.enemy_pos_weight * pos_score

                        next_step = self.do_ai_step(chessboard, get_other_color(color), cur_deep + 1, cur_score,
                                                    lim_cur_score)
                        next_step_score = next_step[1]
                        cur_log += next_step[2]
                        cur_score += next_step_score

                        rollback_step(chessboard, movement)

                        if color is self.color and cur_score >= lim_cur_score or \
                                color is not self.color and cur_score <= lim_cur_score or lim_cur_steps is None:
                            lim_cur_score = cur_score
                            lim_cur_steps = cur_steps
                            lim_cur_log = cur_log
                            lim_cur_log_score = cur_score - next_step_score

                        if cur_deep == 0 and self.info_output:
                            print(make_log(chessboard, cur_steps, cur_score))

                        # условия оптимизации
                        if self.do_alpha_beta_optimize(color, cur_deep, cur_score, prev_score, lim_prev_score):
                            return cur_steps, cur_score, lim_cur_log

        lim_cur_log.insert(0, make_log(chessboard, lim_cur_steps, lim_cur_log_score))

        if cur_deep == 0 and self.info_output:
            print("Best", make_log(chessboard, lim_cur_steps, lim_cur_score))
            print("log:", lim_cur_log)

        return lim_cur_steps, lim_cur_score, lim_cur_log

    def do_alpha_beta_optimize(self, color, cur_deep, cur_score, prev_score, lim_prev_score):
        if cur_deep != 0 and color is self.color and cur_score + prev_score > lim_prev_score:
            return True
        elif cur_deep != 0 and color is not self.color and cur_score + prev_score < lim_prev_score:
            return True
        return False

    def __str__(self):
        return f"class CHESSME_AI({self.difficulty.dif})"


def main():
    pass


if __name__ == "main":
    main()
