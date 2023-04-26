#!/usr/bin/python3
# requires python 3.9+
import itertools
import random


class Holesweeper:
    def __init__(self, field_size: int, num_holes: int):
        self.size = field_size
        self.num_holes = num_holes
        self.board = [[0 for _ in range(field_size)] for _ in range(field_size)]
        self.visible = [[False for _ in range(field_size)] for _ in range(field_size)]
        self.holes = set()
        self.cells_opened = 0
        self.game_over = False
        self.win = False
        self.generate_board()

    def generate_board(self):
        if self.num_holes > self.size ** 2:
            raise Exception("Too much holes")
        # Generate holes
        while len(self.holes) < self.num_holes:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in self.holes:
                self.board[x][y] = -1
                self.holes.add((x, y))
        # Place number for holes cell neighbors
        for x, y in self.holes:
            for dx, dy in itertools.product([-1, 0, 1], repeat=2):
                if dx == dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] != -1:
                    self.board[nx][ny] += 1

    def print_board(self):
        padding = len(str(self.size))
        print("  " + " ".join(f'{(i + 1):{padding}}' for i in range(self.size)))
        for i in range(self.size):
            print(f"{i + 1:{padding}}|" + " ".join(f"{self.get_cell_value(i, j):{padding}}" for j in range(self.size)))

    def get_cell_value(self, x, y):
        if self.visible[x][y]:
            if self.board[x][y] == -1:
                return "*"
            else:
                return str(self.board[x][y])
        else:
            return " "

    def click(self, x, y):
        self.visible[x][y] = True
        self.cells_opened += 1
        if (x, y) in self.holes:
            self.game_over = True
            for x, y in self.holes:
                self.visible[x][y] = True
            self.win = False
        elif self.cells_opened == self.size ** 2 - num_holes:
            # all non hole cells are opened
            self.game_over = True
            self.win = True

        if self.board[x][y] == 0:
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.size and 0 <= ny < self.size and not self.visible[nx][ny]:
                        self.click(nx, ny)

    def safe_cell_input(self, text: str) -> int:
        while True:
            input_str: str = input(text)
            if not input_str.isnumeric() or 1 > (coord := int(input_str)) > self.size:
                print(f"Please enter a number between 0 and {self.size}")
            else:
                # Convert human-readable to computer readable
                return coord - 1

    def play(self):
        while not self.game_over:
            self.print_board()
            x = self.safe_cell_input("Enter row: ")
            y = self.safe_cell_input("Enter column: ")
            self.click(x, y)
        self.print_board()
        if self.win:
            print("You win")
        else:
            print("You lost")


def main():
    size = int(input("Enter board size: "))
    num_holes = int(input("Enter number of holes: "))
    game = Holesweeper(size, num_holes)
    game.play()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
