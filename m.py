import random
import tkinter as tk
import streamlit as st

# --- Configuration Constants ---
GAME_WIDTH = 600
GAME_HEIGHT = 500
SPEED = 100  # Lower number = faster speed (milliseconds per move)
SPACE_SIZE = 20  # Size of grid squares in pixels
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#111111"


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Start at the top-left section of the screen
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        # Align spawn grid to match SPACE_SIZE
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        self.square = canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Classic Snake Game - Tkinter")
        self.root.resizable(False, False)

        self.score = 0
        self.direction = "down"
        self.paused = False
        self.game_over_flag = False

        # --- UI Labels & Canvas ---
        self.score_label = tk.Label(
            root, text=f"Score: {self.score}", font=("Consolas", 20), bg="#222", fg="#FFF"
        )
        self.score_label.pack(fill=tk.X)

        self.canvas = tk.Canvas(
            root, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH
        )
        self.canvas.pack()

        # Center the window on the screen
        self.center_window()

        # Key Bindings
        self.root.bind("<Left>", lambda event: self.change_direction("left"))
        self.root.bind("<Right>", lambda event: self.change_direction("right"))
        self.root.bind("<Up>", lambda event: self.change_direction("up"))
        self.root.bind("<Down>", lambda event: self.change_direction("down"))
        self.root.bind("a", lambda event: self.change_direction("left"))
        self.root.bind("d", lambda event: self.change_direction("right"))
        self.root.bind("w", lambda event: self.change_direction("up"))
        self.root.bind("s", lambda event: self.change_direction("down"))
        self.root.bind("<space>", lambda event: self.toggle_pause())
        self.root.bind("r", lambda event: self.restart())

        # Game Initialization
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)

        self.next_turn()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def change_direction(self, new_direction):
        if self.paused or self.game_over_flag:
            return

        # Prevent 180-degree instant turns
        if new_direction == "left" and self.direction != "right":
            self.direction = new_direction
        elif new_direction == "right" and self.direction != "left":
            self.direction = new_direction
        elif new_direction == "up" and self.direction != "down":
            self.direction = new_direction
        elif new_direction == "down" and self.direction != "up":
            self.direction = new_direction

    def toggle_pause(self):
        if self.game_over_flag:
            return
        self.paused = not self.paused
        if not self.paused:
            self.canvas.delete("pause_text")
            self.next_turn()
        else:
            self.canvas.create_text(
                GAME_WIDTH / 2,
                GAME_HEIGHT / 2,
                text="PAUSED",
                fill="yellow",
                font=("Consolas", 35, "bold"),
                tag="pause_text",
            )

    def next_turn(self):
        if self.paused or self.game_over_flag:
            return

        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= SPACE_SIZE
        elif self.direction == "down":
            y += SPACE_SIZE
        elif self.direction == "left":
            x -= SPACE_SIZE
        elif self.direction == "right":
            x += SPACE_SIZE

        # Insert new head coordinates
        self.snake.coordinates.insert(0, [x, y])

        square = self.canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )
        self.snake.squares.insert(0, square)

        # Check for food collision
        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas)
        else:
            # Delete tail if no food eaten
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Check for collisions
        if self.check_collisions():
            self.game_over()
        else:
            self.root.after(SPEED, self.next_turn)

    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        # Wall collisions
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

        # Self collisions
        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False

    def game_over(self):
        self.game_over_flag = True
        self.canvas.delete("all")
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 - 20,
            text="GAME OVER",
            fill="red",
            font=("Consolas", 40, "bold"),
        )
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2 + 30,
            text=f"Final Score: {self.score}\nPress 'R' to Restart",
            fill="white",
            font=("Consolas", 18),
            justify=tk.CENTER,
        )

    def restart(self):
        if not self.game_over_flag and not self.paused:
            return

        self.score = 0
        self.direction = "down"
        self.game_over_flag = False
        self.paused = False

        self.score_label.config(text=f"Score: {self.score}")
        self.canvas.delete("all")

        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)
        self.next_turn()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()