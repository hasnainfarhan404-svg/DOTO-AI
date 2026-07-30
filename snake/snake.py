import tkinter as tk
import streamlit as st
import random


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.window.resizable(False, False)

        # Game settings
        self.cell_size = 25
        self.grid_width = 20
        self.grid_height = 20
        self.canvas_size = self.cell_size * self.grid_width

        # Direction mappings
        self.directions = {
            "Up": (0, -1),
            "Down": (0, 1),
            "Left": (-1, 0),
            "Right": (1, 0),
        }

        # Game state
        self.score = 0
        self.high_score = 0
        self.snake = []
        self.food = None
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_over = False
        self.speed = 100  # milliseconds per frame

        # Create canvas
        self.canvas = tk.Canvas(
            self.window, width=self.canvas_size, height=self.canvas_size, bg="black"
        )
        self.canvas.pack()

        # Score label
        self.score_label = tk.Label(
            self.window, text="Score: 0  |  High Score: 0", font=("Arial", 14)
        )
        self.score_label.pack(pady=5)

        # Status label
        self.status_label = tk.Label(
            self.window, text="Press SPACE to start", font=("Arial", 11)
        )
        self.status_label.pack(pady=2)

        # Key bindings
        self.window.bind("<KeyPress>", self.change_direction)
        self.window.bind("<Button-1>", self.start_game)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Draw grid
        self.draw_grid()

        self.window.mainloop()

    def draw_grid(self):
        """Draw a subtle grid on the canvas."""
        self.canvas.delete("grid")
        for i in range(0, self.canvas_size, self.cell_size):
            self.canvas.create_line(
                i, 0, i, self.canvas_size, fill="#1a1a1a", tags="grid"
            )
            self.canvas.create_line(
                0, i, self.canvas_size, i, fill="#1a1a1a", tags="grid"
            )

    def start_game(self, event=None):
        """Start or restart the game."""
        if self.game_over:
            self.restart_game()
            return

        if self.snake:
            return  # Game already running

        self.game_over = False
        self.score = 0
        self.speed = 100
        self.direction = "Right"
        self.next_direction = "Right"

        # Initialize snake in the middle
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        for i in range(3):
            self.snake.append((start_x - i, start_y))

        self.draw_snake()
        self.place_food()
        self.update_score()
        self.status_label.config(text="Game Running!")
        self.next_turn()

    def restart_game(self):
        """Reset and restart the game."""
        self.canvas.delete("all")
        self.snake = []
        self.food = None
        self.game_over = False
        self.draw_grid()
        self.start_game()

    def place_food(self):
        """Place food at a random position not occupied by the snake."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                break

        self.food = (x, y)
        fx = x * self.cell_size + self.cell_size // 2
        fy = y * self.cell_size + self.cell_size // 2
        self.canvas.create_oval(
            fx - 8, fy - 8, fx + 8, fy + 8, fill="red", outline="darkred", tags="food"
        )

    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.snake):
            bx = x * self.cell_size
            by = y * self.cell_size
            color = "#00FF00" if i == 0 else "#00CC00"  # Head is brighter
            outline_color = "#003300"
            self.canvas.create_rectangle(
                bx + 1, by + 1, bx + self.cell_size - 1, by + self.cell_size - 1,
                fill=color, outline=outline_color, tags="snake",
            )

    def change_direction(self, event):
        """Change snake direction based on key press."""
        key = event.keysym
        opposite = {
            "Up": "Down", "Down": "Up",
            "Left": "Right", "Right": "Left",
        }

        if key in self.directions:
            # Prevent 180-degree turns
            if opposite.get(key) != self.direction:
                self.next_direction = key

        # Allow restart on game over
        if self.game_over and key == "space":
            self.restart_game()

    def next_turn(self):
        """Execute one turn of the game loop."""
        if self.game_over:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.directions[self.direction]
        new_head = (head_x + dx, head_y + dy)

        # Check wall collision
        if (
            new_head[0] < 0 or new_head[0] >= self.grid_width
            or new_head[1] < 0 or new_head[1] >= self.grid_height
        ):
            self.end_game("Hit the wall!")
            return

        # Check self collision
        if new_head in self.snake:
            self.end_game("Ate itself!")
            return

        # Move snake
        self.snake.insert(0, new_head)

        # Check food
        if new_head == self.food:
            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score
            self.update_score()
            self.canvas.delete("food")
            self.place_food()
            # Increase speed slightly
            if self.speed > 50:
                self.speed -= 2
        else:
            # Remove tail
            self.snake.pop()

        self.draw_snake()
        self.window.after(self.speed, self.next_turn)

    def update_score(self):
        """Update the score display."""
        self.score_label.config(
            text=f"Score: {self.score}  |  High Score: {self.high_score}"
        )

    def end_game(self, reason):
        """End the game."""
        self.game_over = True
        self.status_label.config(text=f"Game Over! ({reason}) Press SPACE to restart")

        # Draw game over text
        self.canvas.delete("over")
        cx = self.canvas_size // 2
        cy = self.canvas_size // 2
        self.canvas.create_text(
            cx, cy - 20, text="GAME OVER", fill="red",
            font=("Arial", 24, "bold"), tags="over",
        )
        self.canvas.create_text(
            cx, cy + 20, text=f"Final Score: {self.score}", fill="white",
            font=("Arial", 14), tags="over",
        )
        self.canvas.create_text(
            cx, cy + 50, text="Press SPACE or click to restart", fill="gray",
            font=("Arial", 10), tags="over",
        )

    def on_closing(self):
        """Handle window close."""
        self.window.destroy()


if __name__ == "__main__":
    SnakeGame()