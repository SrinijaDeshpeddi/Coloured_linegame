import random
import tkinter as tk
from PIL import Image, ImageTk
import pygame

EMPTY_CELL = " "
BALL_COLORS = ["Red", "Green", "Blue", "Yellow", "White"]
BOARD_SIZE = 9
NUM_START_BALLS = 3
WINNING_THRESHOLD = 5
BALL_SCORE = 2
pygame.mixer.init()
pygame.mixer.music.load("C:\\Users\\farha\\Downloads\\background.mp3")
pygame.mixer.music.play(-1)  

remove_sound = pygame.mixer.Sound("C:\\Users\\farha\\Downloads\\bubble-pop.mp3")

class EndGameWindow:
    def __init__(self):
        self.end_window = tk.Tk()
        self.end_window.attributes('-fullscreen', True)  # Set full screen attribute
        self.end_label = tk.Label(self.end_window, text="Game Over", font=("blue", 80), fg="red")
        self.end_label.pack(pady=100, expand=True, anchor="center")
        def close():
            self.end_window.quit()
            self.end_window.destroy()
        self.btn=tk.Button(self.end_window,text="EXIT",bg="red",command=close)
        self.btn.pack()
        pygame.mixer.music.load("C:\\Users\\farha\\Downloads\\gameover.wav")
        pygame.mixer.music.play()  # Play the game over music


class BallGameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)  # Set fullscreen mode
        self.canvas = tk.Canvas(self.window, width=self.window.winfo_screenwidth() - 200,
                                height=self.window.winfo_screenheight())
        self.canvas.pack(side="left")

        self.canvas.pack()
        self.board = [[EMPTY_CELL for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.score = 0
        self.selected_ball = None
        self.game_over = False
        self.initialize_board()
        self.drop_balls()
        self.draw_board()
        self.score_frame = tk.Frame(self.window)
        self.score_frame = tk.Frame(self.window)
        self.score_frame.pack(side="right", padx=10, pady=10, fill="y")

        self.score_label = tk.Label(self.window, text="Score: " + str(self.score), font=("Arial", 16))
        self.score_label.pack(side="top", padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.on_click)
        self.resume_button = tk.Button(self.window, text="Resume", command=self.close_window, bg="blue", fg="white")
        self.resume_button.pack()
        self.resume_button.place(relx=0.8, rely=0.05, relwidth=0.15, relheight=0.07)
        self.exit_button = tk.Button(self.window, text="Exit", command=self.window.quit, bg="black", fg="white")
        self.exit_button.pack()
        self.exit_button.place(relx=0.8, rely=0.13, relwidth=0.15, relheight=0.07)

    def close_window(self):
        self.window.destroy()

    def initialize_board(self):
        random_indices = []
        for i in range(NUM_START_BALLS):
            random_indices.append((random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)))
        for index in random_indices:
            self.board[index[0]][index[1]] = random.choice(BALL_COLORS)

    def end_game(self):
        self.window.destroy()
        game2 = EndGameWindow()
        game2.end_window.mainloop()

    def check_if_full(self):
        empty = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == EMPTY_CELL:
                    empty += 1
        if empty < 3:
            return True
        else:
            return False

    def drop_balls(self):
        if self.check_if_full():
            self.end_game()
        for _ in range(NUM_START_BALLS):
            x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
            color = random.choice(BALL_COLORS)
            while self.board[x][y] != EMPTY_CELL:
                x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
            self.board[x][y] = color
        if self.check_if_full():
            self.end_game()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                x1, y1 = j * 100, i * 95
                x2, y2 = (j + 1) * 100, (i + 1) * 95
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="white")
                if self.board[i][j] != EMPTY_CELL:
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=self.board[i][j])

    def move_ball(self, x_from, y_from, x_to, y_to):
        if self.board[x_from][y_from] != EMPTY_CELL and self.board[x_to][y_to] == EMPTY_CELL:
            self.board[x_to][y_to] = self.board[x_from][y_from]
            self.board[x_from][y_from] = EMPTY_CELL
            self.draw_board()

    def remove_balls_horizontal(self, x, y, color):
        count = 0
        left, right = y, y

        while left >= 0 and self.board[x][left] == color:
            left -= 1

        while right < BOARD_SIZE and self.board[x][right] == color:
            right += 1

        if right - left - 1 >= WINNING_THRESHOLD:
            count += right - left - 1
            for i in range(left + 1, right):
                self.board[x][i] = EMPTY_CELL
            remove_sound.play()  # Play the remove sound effect

        return count

    def remove_balls_vertical(self, x, y, color):
        count = 0
        top, bottom = x, x

        while top >= 0 and self.board[top][y] == color:
            top -= 1

        while bottom < BOARD_SIZE and self.board[bottom][y] == color:
            bottom += 1

        if bottom - top - 1 >= WINNING_THRESHOLD:
            count += bottom - top - 1
            for i in range(top + 1, bottom):
                self.board[i][y] = EMPTY_CELL
            remove_sound.play()  # Play the remove sound effect

        return count

    def remove_balls_diagonal_forward(self, x, y, color):
        count = 0
        top, bottom, left, right = x, x, y, y

        while top >= 0 and left >= 0 and self.board[top][left] == color:
            top -= 1
            left -= 1

        while bottom < BOARD_SIZE and right < BOARD_SIZE and self.board[bottom][right] == color:
            bottom += 1
            right += 1

        if bottom - top - 1 >= WINNING_THRESHOLD:
            count += bottom - top - 1
            for i in range(1,bottom-top):
                self.board[top+i][left+i] = EMPTY_CELL
            remove_sound.play()  # Play the remove sound effect

        return count

    def remove_balls_diagonal_backward(self, x, y, color):
        count = 0
        top, bottom, left, right = x, x, y, y

        while top >= 0 and right < BOARD_SIZE and self.board[top][right] == color:
            top -= 1
            right += 1

        while bottom < BOARD_SIZE and left >= 0 and self.board[bottom][left] == color:
            bottom += 1
            left -= 1

        if bottom - top - 1 >= WINNING_THRESHOLD:
            count += bottom - top - 1
            for i in range(1,bottom-top):
                self.board[top+i][right-i] = EMPTY_CELL
            remove_sound.play()  # Play the remove sound effect

        return count
    def remove_lines(self):
        removed_balls = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != EMPTY_CELL:
                    color = self.board[x][y]
                    count_horizontal = self.remove_balls_horizontal(x, y, color)
                    count_vertical = self.remove_balls_vertical(x, y, color)
                    count_diagonal_forward = self.remove_balls_diagonal_forward(x, y, color)
                    count_diagonal_backward = self.remove_balls_diagonal_backward(x, y, color)
                    count = max(count_horizontal, count_vertical, count_diagonal_forward, count_diagonal_backward)
                    if count >= WINNING_THRESHOLD:
                        removed_balls += count
        return removed_balls

    def calculate_score(self, removed_balls):
        score= removed_balls*BALL_SCORE
        self.score+=score
        self.score_label.config(text="Score:"+str(self.score))
        return score

    def on_click(self, event):

        x = event.y // 95
        y = event.x // 100
        if self.selected_ball is None:
            if self.board[x][y] != EMPTY_CELL:
                self.selected_ball = (x, y)
                self.draw_board()
        else:
            if self.selected_ball == (x, y):
                self.selected_ball = None
                self.draw_board()
            else:
                x_from, y_from = self.selected_ball
                self.move_ball(x_from, y_from, x, y)
                self.selected_ball = None
                removed_balls = self.remove_lines()
                if removed_balls == 0:
                    self.drop_balls()
                else:
                    self.score += self.calculate_score(removed_balls)
                    print("Removed Balls:", removed_balls)
                    print("Your Final Score:", self.score)
                self.draw_board()

class StartWindow:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("Ball Game")
        self.parent.configure(background="red")  # Set background color for the start window

        # Load and resize the image
        image = Image.open(r"C:\\Users\\farha\\OneDrive\\Pictures\\game1.jpg")
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        image = image.resize((screen_width, screen_height))

        # Convert the image to tkinter format
        photo = ImageTk.PhotoImage(image)

        # Create a label to display the image
        self.image_label = tk.Label(self.parent, image=photo)
        self.image_label.image = photo  # Save a reference to avoid garbage collection
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.start_btn = tk.Button(self.parent, text="Start Game", command=self.start_game, bg="green", fg="white")
        self.start_btn.place(relx=0.8, rely=0.5, relwidth=0.2, relheight=0.1)
    def start_game(self):
        self.parent.destroy()
        game = BallGameGUI()
        game.window.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    start_window = StartWindow(root)
    root.mainloop()