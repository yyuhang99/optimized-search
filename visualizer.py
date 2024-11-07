import pygame
import random
import sys
from pathfinding import Pathfinding
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 40  # Default cell size for the grid

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = BLACK
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = font.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

# Set up input boxes for rows, columns, and obstacles
row_input = InputBox(220, 100, 140, 32, "Rows")
col_input = InputBox(220, 150, 140, 32, "Cols")
obstacle_input = InputBox(220, 200, 140, 32, "Obstacles")
input_boxes = [row_input, col_input, obstacle_input]

# Button
button_rect = pygame.Rect(220, 250, 140, 50)

# Main Menu to set up the grid
def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Grid Setup Menu")
    
    while True:
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    try:
                        rows = int(row_input.text)
                        cols = int(col_input.text)
                        obstacles = int(obstacle_input.text)
                        start_game(rows, cols, obstacles)
                    except ValueError:
                        print("Please enter valid numbers.")

        # Draw input boxes and button
        for box in input_boxes:
            box.draw(screen)
        
        # Draw start button
        pygame.draw.rect(screen, BLACK, button_rect)
        start_text = font.render("Start Game", True, WHITE)
        screen.blit(start_text, (button_rect.x + 20, button_rect.y + 10))

        pygame.display.flip()

# Start the game with the selected grid settings
def start_game(rows, cols, obstacles):
    global CELL_SIZE, ROWS, COLS, grid, screen

    ROWS, COLS = rows, cols
    CELL_SIZE = WIDTH // max(rows, cols)  # Calculate cell size based on grid dimensions

    # Initialize screen for gameplay
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pathfinding Visualization")

    # Initialize grid and place obstacles
    grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    start = (0, 0)
    goal = (ROWS - 1, COLS - 1)
    grid[start[0]][start[1]] = 1
    grid[goal[0]][goal[1]] = 2

    for _ in range(obstacles):
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (x, y) != start and (x, y) != goal:
            grid[x][y] = -1

    run_game(start, goal)

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid[row][col] == -1:  # Obstacle
                color = BLACK
            elif grid[row][col] == 1:  # Start
                color = GREEN
            elif grid[row][col] == 2:  # Goal
                color = RED
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Grid lines

# Game loop
def run_game(start, goal):
    # Initialize Pathfinding object
    pathfinder = Pathfinding(grid, start, goal)
    path = pathfinder.d_star()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Draw grid and path
        screen.fill(WHITE)
        draw_grid()

        # Visualize the path
        if path:
            for pos in path:
                pygame.draw.rect(screen, GREEN, (pos[1] * CELL_SIZE, pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()

    pygame.quit()
# Run the main menu to begin
main_menu()
