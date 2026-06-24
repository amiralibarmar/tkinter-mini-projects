import tkinter as tk
from tkinter import ttk
import random

GRID_SIZE = 30
GRID_COUNT = 20
WIDTH = GRID_SIZE * GRID_COUNT
HEIGHT = GRID_SIZE * GRID_COUNT


class Snake:
    def __init__(self, canvas):
        self.canvas = canvas
        self.body = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.grew = False
    
    def draw(self):
        self.canvas.delete("snake")
        for i, (x, y) in enumerate(self.body):
            x1 = x * GRID_SIZE + 3
            y1 = y * GRID_SIZE + 3
            x2 = x1 + GRID_SIZE - 6
            y2 = y1 + GRID_SIZE - 6
            if i == 0:
                self.canvas.create_oval(x1, y1, x2, y2, fill="green", tags="snake")
                self._draw_eyes(x1, y1, x2, y2)
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="lime green", tags="snake")
    
    def _draw_eyes(self, x1, y1, x2, y2):
        dx, dy =self.direction
        cx =(x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = 2
        
        if dx == 1:
            e1 = (x2 - 5, y1 + 4)
            e2 = (x2 - 5, y2 - 6)
        elif dx == -1:
            e1 = (x1 + 3, y1 + 4)
            e2 = (x1 + 3, y2 - 6)
        elif dy == -1:
            e1 = (x1 + 4, y1 + 3)
            e2 = (x2 - 6, y1 +3)
        else:
            e1 = (x1 +4, y2 - 5)
            e2 = (x2 -6, y2 - 5)
        
        for ex, ey in (e1, e2):
            self.canvas.create_oval(ex, ey, ex + r*2, ey + r*2, fill="white", tags="snake")
    
    def move(self):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.body.insert(0, new_head)
        if self.grew:
            self.grew = False
        else:
            self.body.pop()
    
    def grow(self):
        self.grew = True
    
    def change_direction(self, new_dir):
        opposite = (-self.direction[0], -self.direction[1])
        if new_dir != opposite:
            self.next_direction = new_dir


class Food:
    def __init__(self, canvas):
        self.canvas = canvas
        self.position = (0, 0)
        self.randomize()
    
    def randomize(self, snake_body=None):
        while True:
            x = random.randint(0, GRID_COUNT - 1)
            y = random.randint(0, GRID_COUNT - 1)
            if snake_body is None or (x, y) not in snake_body:
                self.position = (x, y)
                break
    
    def draw(self):
        self.canvas.delete("food")
        x, y = self.position
        cx = x * GRID_SIZE + GRID_SIZE // 2  
        cy = y * GRID_SIZE + GRID_SIZE // 2
        r = GRID_SIZE // 4                   
        self.canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="red", tags="food")



class TheGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()
        
        self.score = 0
        self.speed = 150
        self.started = False
        self.binds()
        self.start_screen()
    
    def start_screen(self):
        self.canvas.delete("all")
        if hasattr(self, 'scale') and self.scale.winfo_exists():
            self.scale.destroy()
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2 - 50, text="SNAKE GAME", fill="white", font=("Arial", 32, "bold"))

        self.scale = tk.Scale(self.root, from_=1, to=3, orient="horizontal", label="Difficulty: (E / M / H)", showvalue=False, bg="black", fg="white", highlightthickness=0, troughcolor="#333333", length=150)
        self.scale.set(2)
        
        self.canvas.create_window(WIDTH//2, HEIGHT//2 + 10, window=self.scale)
        
        btn = tk.Button(self.root, text="Start", font=("Arial", 14), bg="lime green", command=self.start_game)
        self.canvas.create_window(WIDTH//2, HEIGHT//2 + 60, window=btn)
    
    def start_game(self):
        self.started = True
        self.score = 0
        self.canvas.delete("all")
        self.setup()
    
    def setup(self):
        self.snake = Snake(self.canvas)
        self.food = Food(self.canvas)        
        self.draw_grid()
        self.update()
    
    def draw_grid(self):
        for i in range(GRID_COUNT):
            x = i * GRID_SIZE
            self.canvas.create_line(x, 0, x, HEIGHT, fill="#1a1a1a")
            self.canvas.create_line(0, x, WIDTH, x, fill="#1a1a1a")
    
    def update(self):
        speeds = {1 : 200, 2 : 150, 3 : 80}
        self.speed = speeds[self.scale.get()]
        
        self.snake.move()
        head = self.snake.body[0]
        
        if head == self.food.position:
            self.snake.grow()
            self.score += 1
            if len(self.snake.body) == GRID_COUNT ** 2:
                self.win()
                return
            self.food.randomize(self.snake.body)
        
        hx ,hy = head
        if not (0 <= hx < GRID_COUNT and 0 <= hy < GRID_COUNT):
            self.game_over()
            return
        
        if self.snake.body.count(head) > 1:
            self.game_over()
            return
        
        self.snake.draw()
        self.food.draw()
        self.draw_hud()
        self.root.after(self.speed, self.update)
    
    def game_over(self):
        self.started = False
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 20, text="GAME OVER", fill="white", font=("Arial", 28, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 20, text=f"Score: {self.score}", fill="yellow", font=("Arial", 18))
        
        btn = tk.Button(self.root, text="Restart", font=("Arial", 14), bg="white", command=self.restart)
        self.canvas.create_window(WIDTH//2, HEIGHT//2 + 50, window=btn)
    
    def restart(self):
        self.score = 0
        self.started = False
        self.canvas.delete("all")
        self.start_screen()
    
    def binds(self, *args):
        self.root.bind("<Up>", lambda e: self._key_press((0, -1)))
        self.root.bind("<Down>", lambda e: self._key_press((0, 1)))
        self.root.bind("<Left>", lambda e: self._key_press((-1, 0)))
        self.root.bind("<Right>", lambda e: self._key_press((1, 0)))
    
    def _key_press(self, direction):
        if not self.started:
            self.start_game()
        self.snake.change_direction(direction)
    
    def draw_hud(self):
        labels = {1 : "Easy", 2 : "Medium", 3 : "Hard"}
        diff_text = labels[self.scale.get()]
        self.canvas.delete("hud")
        self.canvas.create_text(10, 10, anchor="nw", text=f"Score: {self.score}",fill="white", font=("Arial", 12, "bold"), tags="hud")
        self.canvas.create_text(WIDTH - 10, 10, anchor="ne", text=f"Difficulty: {diff_text}", fill="gray", font=("Arial", 12), tags="hud")
    
    def win(self):
        self.started = False
        self.canvas.delete("all")
        self.canvas.create_text(WIDTH//2, HEIGHT//2 - 40, text="YOU WIN! 🎉", fill="lime green", font=("Arial", 32, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 10, text=f"Score: {self.score}", fill="yellow", font=("Arial", 18))
        btn = tk.Button(self.root, text="Play Again", font=("Arial", 14), bg="lime green", command=self.restart)
        self.canvas.create_window(WIDTH//2, HEIGHT//2 + 60, window=btn)






if __name__ == "__main__":
    root = tk.Tk()
    app = TheGame(root)
    root.mainloop()