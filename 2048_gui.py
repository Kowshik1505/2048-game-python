import tkinter as tk
from tkinter import messagebox
import random

GRID_SIZE = 4
BACKGROUND_COLOR = "#92877d"
EMPTY_CELL_COLOR = "#9e948a"

TILE_COLORS = {
    2: "#eee4da",
    4: "#ede0c8",
    8: "#f2b179",
    16: "#f59563",
    32: "#f67c5f",
    64: "#f65e3b",
    128: "#edcf72",
    256: "#edcc61",
    512: "#edc850",
    1024: "#edc53f",
    2048: "#edc22e"
}


class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")

        self.score = 0

        self.score_label = tk.Label(
            root,
            text="Score: 0",
            font=("Arial", 16, "bold")
        )
        self.score_label.grid(row=0, column=0)

        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

        self.frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        self.frame.grid(row=1, column=0)

        self.cells = []

        for i in range(GRID_SIZE):
            row = []

            for j in range(GRID_SIZE):
                cell = tk.Label(
                    self.frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Arial", 24, "bold"),
                    bg=EMPTY_CELL_COLOR,
                    relief="ridge",
                    bd=5
                )

                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)

            self.cells.append(row)

        self.add_tile()
        self.add_tile()

        self.update_gui()

        self.root.bind("<Key>", self.key_press)

    def add_tile(self):
        empty = []

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    empty.append((i, j))

        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2

    def update_gui(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):

                value = self.board[i][j]

                if value == 0:
                    self.cells[i][j].config(
                        text="",
                        bg=EMPTY_CELL_COLOR
                    )
                else:
                    self.cells[i][j].config(
                        text=str(value),
                        bg=TILE_COLORS.get(value, "#3c3a32")
                    )

        self.score_label.config(text=f"Score: {self.score}")

    def compress(self, row):
        new_row = [num for num in row if num != 0]

        i = 0
        while i < len(new_row) - 1:

            if new_row[i] == new_row[i + 1]:

                new_row[i] *= 2
                self.score += new_row[i]

                new_row.pop(i + 1)

            i += 1

        new_row += [0] * (GRID_SIZE - len(new_row))

        return new_row

    def move_left(self):
        changed = False

        for i in range(GRID_SIZE):

            original = self.board[i][:]

            self.board[i] = self.compress(self.board[i])

            if original != self.board[i]:
                changed = True

        return changed

    def move_right(self):
        changed = False

        for i in range(GRID_SIZE):

            original = self.board[i][:]

            row = self.board[i][::-1]
            row = self.compress(row)

            self.board[i] = row[::-1]

            if original != self.board[i]:
                changed = True

        return changed

    def transpose(self):
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def game_over(self):

        for row in self.board:
            if 0 in row:
                return False

        for i in range(4):
            for j in range(3):
                if self.board[i][j] == self.board[i][j + 1]:
                    return False

        for j in range(4):
            for i in range(3):
                if self.board[i][j] == self.board[i + 1][j]:
                    return False

        return True

    def key_press(self, event):

        changed = False

        if event.keysym == "Left":
            changed = self.move_left()

        elif event.keysym == "Right":
            changed = self.move_right()

        elif event.keysym == "Up":
            changed = self.move_up()

        elif event.keysym == "Down":
            changed = self.move_down()

        if changed:

            self.add_tile()
            self.update_gui()

            for row in self.board:
                if 2048 in row:
                    messagebox.showinfo(
                        "You Won!",
                        f"Congratulations!\n\nScore: {self.score}"
                    )
                    return

            if self.game_over():
                messagebox.showerror(
                    "Game Over",
                    f"No more moves left!\n\nFinal Score: {self.score}"
                )


root = tk.Tk()
game = Game2048(root)
root.mainloop()