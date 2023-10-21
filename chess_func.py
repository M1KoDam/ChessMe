from chessboard import *
from math_helper import sgn_vector, sgn
from math import ceil
from Enums.steps import *
from encode_decode import *


class Movement:
    def __init__(self, cur_cell, target_cell, cur_figure, target_figure, step_type=None):
        self.cur_cell = cur_cell
        self.target_cell = target_cell
        self.cur_figure = cur_figure
        self.target_figure = target_figure
        self.step_type = step_type
        self.color = cur_figure.color

        self.target_figure_class = None if target_figure is None else target_figure.__class__
        self.cur_figure_class = cur_figure.__class__

    def __str__(self):
        return f"{self.color.color}: " \
            + make_step_log(self.cur_cell, self.target_cell, self.cur_figure, self.target_figure)


def make_step_log(cur_cell, target_cell, cur_figure, target_figure):
    cur_icon = cur_figure.get_icon()
    step_icon = " " if target_figure is None else target_figure.get_icon()
    return f"{cur_icon}{letter_translation[cur_cell[1]]}{number_translation[cur_cell[0]]}" + \
        "->" + \
        f"{letter_translation[target_cell[1]]}{number_translation[target_cell[0]]}{step_icon}"


def make_log(chessboard, steps, score):
    if steps is None:
        return f"Step: None priority score: 0"
    cur_cell = steps[0]
    target_cell = steps[1]
    cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
    target_figure = chessboard.square[target_cell[0]][target_cell[1]]

    return f"Step: " + make_step_log(cur_cell, target_cell, cur_figure, target_figure) + \
        f"priority score: {score}"


def get_other_color(color):
    """Возвращает противоположный цвет переданному"""
    return White if color is Black else Black


def input_pawn_upgrade(color):
    """Обработка замены пешки на другую фигуру при достижении края"""
    new_figure = None
    while new_figure is None:
        player_input = input(f'Choose figure("P", "K", "B", "R", "Q"): ').strip().lower()
        match player_input:
            case "p":
                new_figure = Pawn(color)
            case "k":
                new_figure = Knight(color)
            case "b":
                new_figure = Bishop(color)
            case "r":
                new_figure = Rook(color)
            case "q":
                new_figure = Queen(color)
            case _:
                print("Incorrect input!")

    return new_figure


def do_step(chessboard, cell, target_cell, out_info=True, pawn_auto_upgrade=False):
    """Ход, возвращает объект movement если ход корректен и None в противном случае"""
    step = Move

    # Инициализация фигур и вектора движения
    figure = chessboard.square[cell[0]][cell[1]]
    target_figure = chessboard.square[target_cell[0]][target_cell[1]]
    cell_vector = (target_cell[0] - cell[0], target_cell[1] - cell[1])
    vector = sgn_vector(cell_vector) if figure.range > 1 else cell_vector

    # Проверка рокировки
    if isinstance(figure, King) and vector in figure.castling:
        movement = handle_castling(chessboard, cell, target_cell, out_info)
        if movement is None:
            return None

    # Проверка возможности попадания на клетку
    elif vector in figure.possible_movements:
        if issubclass(target_figure.__class__, Figure) and target_figure.color == figure.color:
            if out_info:
                print("You can't move there!")
            return None

        # Проверка атаки пешки
        if isinstance(figure, Pawn) and vector in figure.attacks:
            en_passant = (0, vector[1])
            en_passant_figure = chessboard.square[cell[0]+en_passant[0]][cell[1]+en_passant[1]]
            if isinstance(en_passant_figure, Pawn) and en_passant_figure.color != figure.color and \
                    chessboard.movements[-1].cur_figure == en_passant_figure and \
                    abs(chessboard.movements[-1].cur_cell[0] - chessboard.movements[-1].target_cell[0]) == 2:
                target_figure = en_passant_figure
                chessboard.square[cell[0] + en_passant[0]][cell[1] + en_passant[1]] = None
                step = EnPassant
            elif not issubclass(target_figure.__class__, Figure) or target_figure.color == figure.color or cell_vector not in figure.attacks:
                if out_info:
                    print("You can't move there!")
                return None

        # Проверка хода пешки
        if isinstance(figure, Pawn) and vector not in figure.attacks:
            if issubclass(target_figure.__class__, Figure):
                if out_info:
                    print("You can't move there!")
                return None

        # Проверка существования хода
        for r in range(1, figure.range+1):
            step_cell = (cell[0] + vector[0] * r, cell[1] + vector[1] * r)
            if step_cell == target_cell:
                break
        else:
            if out_info:
                print("You can't move there!")
            return None

        # Проверка на преграду на пути
        for r in range(1, figure.range+1):
            step_cell = (cell[0] + vector[0] * r, cell[1] + vector[1] * r)
            step_cell_figure = chessboard.square[step_cell[0]][step_cell[1]]
            if step_cell == target_cell:
                break
            if issubclass(step_cell_figure.__class__, Figure):
                if out_info:
                    print("You can't move there!")
                return None

        chessboard.square[target_cell[0]][target_cell[1]] = figure
        chessboard.square[cell[0]][cell[1]] = None
        figure.move()

        if issubclass(target_figure.__class__, Figure) and step is not EnPassant:
            step = Attack

        movement = Movement(cell, target_cell, figure, target_figure, step)

        if isinstance(figure, Pawn):
            chessboard.square[target_cell[0]][target_cell[1]] = check_pawn_promotion(chessboard, target_cell,
                                                                                     pawn_auto_upgrade)

    else:
        if out_info:
            print("You can't move there!")
        return None

    chessboard.add_movement(movement)

    if is_check(chessboard, figure.color):
        rollback_step(chessboard, movement)
        if out_info:
            print("Your King is under Attack!")
        return None

    return movement


def rollback_step(chessboard, movement):
    tar_figure = None if movement.step_type is EnPassant else movement.target_figure
    chessboard.square[movement.target_cell[0]][movement.target_cell[1]] = tar_figure
    chessboard.square[movement.cur_cell[0]][movement.cur_cell[1]] = movement.cur_figure
    if movement.step_type is EnPassant:
        en_passant_vector = (0, movement.target_cell[1] - movement.cur_cell[1])
        chessboard.square[movement.cur_cell[0] + en_passant_vector[0]][movement.cur_cell[1] + en_passant_vector[1]] = movement.target_figure
    elif movement.step_type is Castling:
        move_vector_w = movement.cur_cell[1] - movement.target_cell[1]
        king_cell = (movement.cur_cell[0], movement.cur_cell[1] - move_vector_w // 2)
        rook_cell = (movement.target_cell[0], movement.target_cell[1] + ceil(move_vector_w / 2) + sgn(move_vector_w))
        chessboard.square[king_cell[0]][king_cell[1]] = None
        chessboard.square[rook_cell[0]][rook_cell[1]] = None
        movement.target_figure.move_back()

    movement.cur_figure.move_back()
    chessboard.delete_movement(movement)


def check_pawn_promotion(chessboard, cell, pawn_auto_upgrade=False):
    """Проверка - достигла ли пешка края"""
    figure = chessboard.square[cell[0]][cell[1]]
    if cell[0] == 7 and figure.color is Black or cell[0] == 0 and figure.color is White:
        if not pawn_auto_upgrade:
            new_figure = input_pawn_upgrade(figure.color)
        else:
            new_figure = Queen(figure.color)
        new_figure.moves_count = figure.moves_count
        figure = new_figure
    return figure


def handle_castling(chessboard, cur_cell, target_cell, out_info):
    """Рокировка"""
    cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
    target_figure = chessboard.square[target_cell[0]][target_cell[1]]
    move_vector = cur_cell[1] - target_cell[1]

    if not (isinstance(target_figure, Rook) and cur_figure.color == target_figure.color) or is_check(chessboard, cur_figure.color):
        if out_info:
            print("You can't move there!!")
        return None

    king_cell = (cur_cell[0], cur_cell[1] - move_vector // 2)
    rook_cell = (target_cell[0], target_cell[1] + ceil(move_vector / 2) + sgn(move_vector))

    # Проверка встречи препятствия на пути рокировки
    for i in range(1, move_vector) if move_vector >= 0 else range(-1, move_vector, -1):
        new_cell = (cur_cell[0], cur_cell[1] - i)
        if chessboard.square[new_cell[0]][new_cell[1]] is target_figure:
            break
        if chessboard.square[new_cell[0]][new_cell[1]] is not None:
            if out_info:
                print("You can't do castling!")
            return None

    chessboard.square[king_cell[0]][king_cell[1]] = cur_figure
    chessboard.square[cur_cell[0]][cur_cell[1]] = None
    chessboard.square[rook_cell[0]][rook_cell[1]] = target_figure
    chessboard.square[target_cell[0]][target_cell[1]] = None
    cur_figure.move()
    target_figure.move()

    movement = Movement(cur_cell, target_cell, cur_figure, target_figure, Castling)

    return movement


def is_draw(chessboard, color):
    """Проверяет на ничью"""
    if chessboard.steps_to_draw[-1] >= 50:
        return True

    desk_representation = {}
    for desk in chessboard.desks:
        if desk in desk_representation.keys():
            desk_representation[desk] += 1
            if desk_representation[desk] >= 3:
                return True
        else:
            desk_representation[desk] = 1

    for w in range(8):
        for h in range(8):
            cur_cell = (w, h)
            cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
            if not (issubclass(cur_figure.__class__, Figure) and cur_figure.color == color):
                continue

            for possible_movement in cur_figure.possible_movements:
                for r in range(1, cur_figure.range + 1):
                    step_cell = (cur_cell[0] + possible_movement[0] * r, cur_cell[1] + possible_movement[1] * r)
                    if step_cell[0] < 0 or step_cell[0] > 7 or step_cell[1] < 0 or step_cell[1] > 7:
                        break

                    movement = do_step(chessboard, cur_cell, step_cell, False, True)
                    if movement:
                        rollback_step(chessboard, movement)
                        return False

    return True


def is_chessboard_draw(chessboard):
    if chessboard.steps_to_draw[-1] == 50:
        return True

    desk_representation = {}
    for desk in chessboard.desks:
        if desk in desk_representation.keys():
            desk_representation[desk] += 1
            if desk_representation[desk] >= 3:
                return True
        else:
            desk_representation[desk] = 1

    return False


def is_checkmate(chessboard, color):
    """Проверяет поставлен ли мат королю передаваемого цвета"""
    for w in range(8):
        for h in range(8):
            cur_cell = (w, h)
            cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
            if not (issubclass(cur_figure.__class__, Figure) and cur_figure.color == color):
                continue

            for possible_movement in cur_figure.possible_movements:
                for r in range(1, cur_figure.range + 1):
                    step_cell = (cur_cell[0] + possible_movement[0] * r, cur_cell[1] + possible_movement[1] * r)
                    if step_cell[0] < 0 or step_cell[0] > 7 or step_cell[1] < 0 or step_cell[1] > 7:
                        break

                    movement = do_step(chessboard, cur_cell, step_cell, False, True)

                    if not movement:
                        continue

                    if not is_check(chessboard, color):
                        rollback_step(chessboard, movement)
                        return False

                    rollback_step(chessboard, movement)

    return True


def is_check(chessboard, color):
    """Проверка на шах, возвращает True,
         если король переданного цвета находится под ударом, в противном случае False"""
    other_turn = get_other_color(color)
    for w in range(8):
        for h in range(8):
            cur_cell = (w, h)
            cur_figure = chessboard.square[cur_cell[0]][cur_cell[1]]
            if not (issubclass(cur_figure.__class__, Figure) and cur_figure.color == other_turn):
                continue

            for possible_movement in cur_figure.possible_movements:
                for r in range(1, cur_figure.range + 1):
                    step_cell = (cur_cell[0] + possible_movement[0] * r, cur_cell[1] + possible_movement[1] * r)
                    if step_cell[0] < 0 or step_cell[0] > 7 or step_cell[1] < 0 or step_cell[1] > 7:
                        break
                    step_cell_figure = chessboard.square[step_cell[0]][step_cell[1]]
                    if isinstance(cur_figure, Pawn) and (possible_movement not in cur_figure.attacks or r > 1):
                        break
                    if isinstance(cur_figure, King) and possible_movement in cur_figure.castling:
                        break
                    if isinstance(step_cell_figure, King) and step_cell_figure.color != other_turn:
                        return True
                    if issubclass(step_cell_figure.__class__, Figure):
                        break

    return False


def main():
    pass


if __name__ == "__main__":
    main()
