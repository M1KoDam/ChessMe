from chess_func import *
from chessboard import Chessboard
from ChessAi import ChessAI
from menu_options import Menu
from player import *
from Enums.difficulties import *
from importlib.machinery import SourceFileLoader


def make_input_clear(guess):
    for i in [" ", ",", "."]:
        guess.replace(i, "")
    return guess


class Program:
    def __init__(self):
        self.PROGRAM_RUNNING = True
        self.GAME_RUNNING = True
        self.turn = White
        self.chessboard = Chessboard()

        self.white_player = Player(White)
        self.black_player = Player(Black)
        self.AI_logo = False
        self.COMMAND_LINE_ACTIVE = True

    def run_program(self):
        print(Menu.greeting)
        while self.PROGRAM_RUNNING:
            self.greeting()

    def new_game(self):
        self.chessboard.clear()
        self.turn = White
        self.AI_logo = False

    def run_game(self):
        self.GAME_RUNNING = True
        while self.GAME_RUNNING:
            player = self.white_player if self.turn is White else self.black_player
            self.chessboard.render_desk()

            # Проверка на шах, мат и ничью
            if self.situation_check(self.turn) or self.situation_check(get_other_color(self.turn)):
                self.GAME_RUNNING = False
                self.new_game()
                continue
            else:
                if is_draw(self.chessboard, self.turn):
                    self.GAME_RUNNING = False
                    self.new_game()
                    print("Draw!")
                    continue

            if self.COMMAND_LINE_ACTIVE:
                if self.handle_event():
                    continue

            movement_cell = player.try_do_step(self.chessboard)
            if not movement_cell:
                continue
            pawn_auto_upgrade = False if player is Player else True
            movement = do_step(self.chessboard, movement_cell[0], movement_cell[1], pawn_auto_upgrade=pawn_auto_upgrade)
            if not movement:
                continue
            print(f"(Move {self.chessboard.moves_count()}) {movement}")

            self.turn = White if self.turn is Black else Black

    def situation_check(self, turn):
        if is_check(self.chessboard, turn):
            if is_checkmate(self.chessboard, turn):
                print(f"Checkmate! {get_other_color(turn).color} Win!")
                return True
            print("Check!")
        return False

    def handle_event(self):
        event = input(">>> Tap to continue: ").lower()
        if event == "menu":
            self.GAME_RUNNING = False
            return True
        if event == "logo":
            self.AI_logo = not self.AI_logo
            if isinstance(self.white_player, ChessAI):
                self.white_player.info_output = self.AI_logo
            if isinstance(self.black_player, ChessAI):
                self.black_player.info_output = self.AI_logo
        return False

    def greeting(self):
        if self.chessboard.moves_count() > 0:
            self.greeting_con()
            return

        print(Menu.start_menu)
        guess = make_input_clear(input(">>> Your choice: ").lower())
        if guess in ("1", "new game", "new"):
            self.new_game()
            self.run_game()
        elif guess in ("2", "load", "load player"):
            self.load_player_color()
        elif guess in ("3", "show", "show player"):
            self.show_players()
        elif guess in ("4", "options", "settings"):
            self.open_options()
        elif guess in ("5", "exit", "quit"):
            self.PROGRAM_RUNNING = False
        else:
            print("Incorrect input")

    def greeting_con(self):
        print(Menu.start_menu_con)
        guess = make_input_clear(input(">>> Your choice: ").lower())
        if guess in ("1", "play", "continue"):
            self.run_game()
        elif guess in ("2", "new game", "new"):
            self.new_game()
            self.run_game()
        elif guess in ("3", "load", "load player"):
            self.load_player_color()
        elif guess in ("4", "show", "show player"):
            self.show_players()
        elif guess in ("5", "options", "settings"):
            self.open_options()
        elif guess in ("6", "exit", "quit"):
            self.PROGRAM_RUNNING = False
        else:
            print("Incorrect input")

    def open_options(self):
        print(f"""
Choose one of the following options:
1. ({'On' if self.COMMAND_LINE_ACTIVE else 'Off'}) Command line
2. Back""")
        guess = make_input_clear(input(">>> Your choice: ").lower())
        if guess in ("1", "play", "continue"):
            self.COMMAND_LINE_ACTIVE = not self.COMMAND_LINE_ACTIVE
            print(f"Command line is {'on' if self.COMMAND_LINE_ACTIVE else 'off'}")
        elif guess in ("2", "back"):
            return
        else:
            print("Incorrect input")

    def show_players(self):
        print(f"\nWhite player: {self.white_player}\n" + f"Black player: {self.black_player}")

    def load_player_color(self):
        print(f"""
Choose player to load:
1. ({self.white_player}) Load white player
2. ({self.black_player}) Load black player
3. Back""")
        guess = make_input_clear(input(">>> Your choice: ").lower())
        if guess in ("1", "white"):
            self.load_player(White)
        elif guess in ("2", "black"):
            self.load_player(Black)
        elif guess in ("3", "back"):
            return
        else:
            print("Incorrect input")

    def load_player(self, color):
        print(Menu.load_player_menu)
        guess = make_input_clear(input(">>> Your choice: ").lower())

        if guess in ("1", "player"):
            self.set_player(color, Player(color))
        elif guess in ("2", "chessme_ai(easy)", "easy"):
            self.set_player(color, ChessAI(color, EASY))
        elif guess in ("3", "chessme_ai(hard)", "hard"):
            self.set_player(color, ChessAI(color, HARD))
        elif guess in ("4", "load"):
            self.load_outsider(color)
        elif guess in ("5", "back"):
            return
        else:
            print("Incorrect input")

    def load_outsider(self, color):
        path = input(">>> Enter path to file: ").strip()
        name = path.split("\\")[-1][:-3]

        try:
            module = SourceFileLoader(name, path).load_module()
            self.set_player(color, module.ChessAI(color))
            print("Successfully")
        except FileNotFoundError:
            print("Error opening the file")
        except AttributeError:
            print("File must contains ChessAI class. Check README file for more information")

    def set_player(self, color, player):
        if color is White:
            self.white_player = player
        else:
            self.black_player = player


def main():
    program = Program()
    program.run_program()


if __name__ == "__main__":
    main()
