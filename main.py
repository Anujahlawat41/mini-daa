import tkinter as tk
import random

GRID_SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 16

BACKGROUND_COLOR = "#bbada0"
FONT = ("Arial", 36, "bold")

# Tile colors
TILE_COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}


class Game2048(tk.Frame):
    def __init__(self):
        super().__init__()
        self.master.title("2048 Game")
        self.grid()
        self.master.resizable(False, False)
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.game_over = False

        # Setup Canvas
        self.canvas = tk.Canvas(
            self,
            width=GRID_SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
            height=GRID_SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
            bg=BACKGROUND_COLOR
        )
        self.canvas.grid()
        self.bind_all("<KeyPress>", self.key_handler)

        # Initialize Game
        self.add_random_tile()
        self.add_random_tile()
        self.draw_board()

    def add_random_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty:
            x, y = random.choice(empty)
            self.board[x][y] = 4 if random.random() > 0.9 else 2

    def rotate_board_clockwise(self):
        self.board = [list(row) for row in zip(*self.board[::-1])]

    def move_left(self):
        moved = False
        for i in range(GRID_SIZE):
            row = [x for x in self.board[i] if x != 0]
            new_row = []
            skip = False
            for j in range(len(row)):
                if skip:
                    skip = False
                    continue
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    new_row.append(row[j] * 2)
                    skip = True
                else:
                    new_row.append(row[j])
            new_row += [0] * (GRID_SIZE - len(new_row))
            if new_row != self.board[i]:
                moved = True
            self.board[i] = new_row
        return moved

    def move(self, direction):
        if direction == "Up":
            rotations = 1
        elif direction == "Right":
            rotations = 2
        elif direction == "Down":
            rotations = 3
        else:
            rotations = 0

        for _ in range(rotations):
            self.rotate_board_clockwise()
        moved = self.move_left()
        for _ in range((4 - rotations) % 4):
            self.rotate_board_clockwise()

        if moved:
            self.add_random_tile()
        self.check_game_over()
        self.draw_board()

    def check_game_over(self):
        for row in self.board:
            if 0 in row:
                return
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 1):
                if self.board[i][j] == self.board[i][j + 1] or self.board[j][i] == self.board[j + 1][i]:
                    return
        self.game_over = True

    def key_handler(self, event):
        """Handle arrow key presses safely"""
        if self.game_over:
            return

        key = event.keysym  # Correct key name property
        if key in ("Left", "Right", "Up", "Down"):
            self.move(key)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.board[i][j]
                color_bg, color_fg = TILE_COLORS.get(value, ("#cdc1b4", "#776e65"))
                x = j * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                y = i * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN
                self.canvas.create_rectangle(
                    x, y, x + TILE_SIZE, y + TILE_SIZE, fill=color_bg, outline=""
                )
                if value != 0:
                    self.canvas.create_text(
                        x + TILE_SIZE / 2,
                        y + TILE_SIZE / 2,
                        text=str(value),
                        fill=color_fg,
                        font=FONT
                    )

        if self.game_over:
            self.canvas.create_rectangle(
                0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(),
                fill="#ffffff", stipple="gray50"
            )
            self.canvas.create_text(
                self.canvas.winfo_width() / 2,
                self.canvas.winfo_height() / 2,
                text="Game Over",
                fill="black",
                font=("Arial", 48, "bold")
            )


if __name__ == "__main__":
    Game2048().mainloop()
