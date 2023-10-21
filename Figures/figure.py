class White:
    color = "White"


class Black:
    color = "Black"


class Figure:
    def __init__(self, color):
        self.color = color
        self.moves_count = 0

    def move(self):
        self.moves_count += 1

    def move_back(self):
        self.moves_count -= 1
        if self.moves_count < 0:
            self.moves_count = 0

    def __str__(self):
        return "figure"

    def copy(self):
        pass
