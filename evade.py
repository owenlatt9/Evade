import tkinter as tk
import random
import math

# --- CONFIGURATION ---
GAME_WIDTH = 1200
GAME_HEIGHT = 800
PLAYER_SIZE = 15
MIN_BALL_SIZE = 15
MAX_BALL_SIZE = 85  # Increased for bigger balls
SPEED_MULTIPLIER = 1.0
MIN_SPEED = 2
MAX_SPEED = 8

root = tk.Tk()
root.title("Evade")
root.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")

start_frame = tk.Frame(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg='black')
start_frame.pack(expand=True, fill='both')

title_label = tk.Label(start_frame, text="Evade", fg="white", bg="black", font=("Helvetica", 40, "bold"))
title_label.place(relx=0.5, rely=0.4, anchor="center")

canvas = tk.Canvas(root, width=GAME_WIDTH, height=GAME_HEIGHT, bg='black')

# Game state
score = 0
game_active = False 
score_text = None
balls = []
ball_spawn_timer = None 

class Ball:
    def __init__(self, canvas, x, y, radius, color, x_speed, y_speed):
        self.canvas = canvas 
        self.radius = radius
        self.x = x
        self.y = y
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.onscreen = False
        self.ball = canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=color
        )

    def move(self):
        if self.on_screen():
            self.onscreen = True
        
        if self.onscreen:
            self.bounce()
            
        self.x += self.x_speed
        self.y += self.y_speed
        self.canvas.move(self.ball, self.x_speed, self.y_speed)

    def bounce(self):
        if (self.x + self.radius) > GAME_WIDTH:
            self.x_speed = -abs(self.x_speed) 
        if (self.x - self.radius) < 0:
            self.x_speed = abs(self.x_speed)
        if (self.y + self.radius) > GAME_HEIGHT:
            self.y_speed = -abs(self.y_speed)
        if (self.y - self.radius) < 0:
            self.y_speed = abs(self.y_speed)

    def on_screen(self):
        x1 = (self.x - self.radius) > 0
        y1 = (self.y - self.radius) > 0
        x2 = (self.x + self.radius) < GAME_WIDTH
        y2 = (self.y + self.radius) < GAME_HEIGHT
        return x1 and x2 and y1 and y2

class CursorBall:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.radius = PLAYER_SIZE
        self.x = GAME_WIDTH // 2
        self.y = GAME_HEIGHT // 2
        self.cursor_ball = canvas.create_oval(
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius,
            fill=color
        )
        canvas.bind("<Motion>", self.update_position)    

    def update_position(self, event):
        x, y = event.x, event.y
        if x < self.radius:
            x = self.radius
        elif x > GAME_WIDTH - self.radius:
            x = GAME_WIDTH - self.radius
        if y < self.radius:
            y = self.radius
        elif y > GAME_HEIGHT - self.radius:
            y = GAME_HEIGHT - self.radius
        self.x, self.y = x, y
        self.canvas.coords(
            self.cursor_ball,
            self.x - self.radius, self.y - self.radius,
            self.x + self.radius, self.y + self.radius
        )

cursor_ball = CursorBall(canvas, 'yellow')

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

def is_collision(ball1, ball2):
    x1, y1, r1 = ball1.x, ball1.y, ball1.radius
    x2, y2, r2 = ball2.x, ball2.y, ball2.radius
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance <= (r1 + r2)

def make_ball():
    # Size and speed are linked: small = fast, big = slow
    size_roll = random.random()  # 0 to 1
    radius = MIN_BALL_SIZE + size_roll * (MAX_BALL_SIZE - MIN_BALL_SIZE)
    speed = (MAX_SPEED - size_roll * (MAX_SPEED - MIN_SPEED)) * SPEED_MULTIPLIER
    
    rand_side = random.randint(1, 4)
    start_x, start_y = 0, 0
    
    if rand_side == 1:  # Top
        start_x = random.randint(int(radius), int(GAME_WIDTH - radius))
        start_y = -radius * 2
    elif rand_side == 2:  # Right
        start_x = GAME_WIDTH + radius * 2
        start_y = random.randint(int(radius), int(GAME_HEIGHT - radius))
    elif rand_side == 3:  # Bottom
        start_x = random.randint(int(radius), int(GAME_WIDTH - radius))
        start_y = GAME_HEIGHT + radius * 2
    elif rand_side == 4:  # Left
        start_x = -radius * 2
        start_y = random.randint(int(radius), int(GAME_HEIGHT - radius))

    # Target the middle third of the screen
    target_x = random.randint(GAME_WIDTH // 3, GAME_WIDTH * 2 // 3)
    target_y = random.randint(GAME_HEIGHT // 3, GAME_HEIGHT * 2 // 3)

    dx = target_x - start_x
    dy = target_y - start_y
    distance = math.sqrt(dx**2 + dy**2)
    
    final_x_speed = (dx / distance) * speed
    final_y_speed = (dy / distance) * speed

    balls.append(Ball(canvas, start_x, start_y, radius, random_color(), final_x_speed, final_y_speed))

def move_balls():
    if not game_active:
        return
    for ball in balls:
        ball.move()
        if is_collision(cursor_ball, ball):
            game_over()
            return
    canvas.tag_raise(cursor_ball.cursor_ball)
    canvas.tag_raise("hud") 
    root.after(16, move_balls)

def game_over():
    global game_active, ball_spawn_timer
    game_active = False 
    
    if ball_spawn_timer is not None:
        root.after_cancel(ball_spawn_timer)
        ball_spawn_timer = None

    canvas.delete("hud")
    center_x = GAME_WIDTH // 2
    center_y = GAME_HEIGHT // 2
    
    canvas.create_text(center_x, center_y - 50, text="GAME OVER", fill="red", font=("Helvetica", 60, "bold"), tags="gameover_ui")
    canvas.create_text(center_x, center_y + 20, text=f"Final Score: {score}", fill="white", font=("Helvetica", 30), tags="gameover_ui")
    
    play_again_btn = tk.Button(root, text="Play Again", command=restart_game, font=("Helvetica", 20), bg="white", fg="black")
    canvas.create_window(center_x, center_y + 100, window=play_again_btn, tags="gameover_ui")

def restart_game():
    global score, game_active, balls, score_text, ball_spawn_timer
    score = 0
    game_active = True
    
    if ball_spawn_timer is not None:
        root.after_cancel(ball_spawn_timer)
        ball_spawn_timer = None

    canvas.delete("gameover_ui")
    canvas.delete("hud") 
    for ball in balls:
        canvas.delete(ball.ball)
    balls.clear()
    
    score_text = canvas.create_text(50, 30, text="Score: 0", fill="white", font=("Helvetica", 20, "bold"), tags="hud")
    make_ball()
    move_balls()
    
    ball_spawn_timer = root.after(3000, add_ball_periodically)

def start_game():
    global game_active, score_text, ball_spawn_timer
    game_active = True 
    start_frame.pack_forget()
    canvas.pack(fill="both", expand=True) 
    score_text = canvas.create_text(50, 30, text="Score: 0", fill="white", font=("Helvetica", 20, "bold"), tags="hud")
    make_ball()
    move_balls()
    
    ball_spawn_timer = root.after(3000, add_ball_periodically)

def add_ball_periodically():
    global ball_spawn_timer
    if not game_active:
        return 
    
    make_ball()
    ball_spawn_timer = root.after(3000, add_ball_periodically)

def game_timer():
    global score 
    if game_active:
        score += 1
        canvas.itemconfig(score_text, text=f"Score: {score}") 
    root.after(1000, game_timer) 

root.after(1000, game_timer)
start_button = tk.Button(start_frame, text="Start Game", command=start_game, font=("Helvetica", 20))
start_button.place(relx=0.5, rely=0.6, anchor="center")

root.mainloop()
