import pygame
import random
from pathfinding import Pathfinding
import threading

pygame.init()

WIDTH, HEIGHT = 1300, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Set fixed window size

ROWS, COLS = 30, 30
CELL_SIZE = min(WIDTH // 2 // COLS, HEIGHT // 2 // ROWS) - 2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

grid_a_star = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid_d_star = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid_jump_search = [[0 for _ in range(COLS)] for _ in range(ROWS)]

start = (0, 0)
goal = (ROWS - 1, COLS - 1)

# Place obstacles
for _ in range(150):
    x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    if (x, y) != start and (x, y) != goal:
        grid_a_star[x][y] = -1
        grid_d_star[x][y] = -1
        grid_jump_search[x][y] = -1

for grid in [grid_a_star, grid_d_star, grid_jump_search]:
    grid[start[0]][start[1]] = 1
    grid[goal[0]][goal[1]] = 2

lock = threading.Lock()

def draw_grid(grid, offset_x, offset_y):
    """Draw the grid on the screen"""
    center_x = offset_x + (WIDTH // 2 - COLS * CELL_SIZE) // 2
    center_y = offset_y + (HEIGHT // 2 - ROWS * CELL_SIZE) // 2
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid[row][col] == -1:  # Obstacle
                color = BLACK
            elif grid[row][col] == 1:  # Start
                color = GREEN
            elif grid[row][col] == 2:  # Goal
                color = RED
            elif grid[row][col] == 3:  # A* Algorithm
                color = ORANGE
            elif grid[row][col] == 4:  # D* Algorithm
                color = YELLOW
            elif grid[row][col] == 5:  # Jump Search Algorithm
                color = BLUE
            pygame.draw.rect(
                screen,
                color,
                (center_x + col * CELL_SIZE, center_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(
                screen,
                BLACK,
                (center_x + col * CELL_SIZE, center_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )


def draw_labels():
    """Draw labels for the visualizations."""
    font = pygame.font.Font(None, 36)
    label_a_star = font.render("A* Algorithm", True, BLACK)
    label_d_star = font.render("D* Algorithm", True, BLACK)
    label_jump_search = font.render("Jump Search Algorithm", True, BLACK)
    
    # Positions for the labels
    screen.blit(label_a_star, (WIDTH // 4 - label_a_star.get_width() // 2, 10))
    screen.blit(label_d_star, (3 * WIDTH // 4 - label_d_star.get_width() // 2, 10))
    screen.blit(label_jump_search, (WIDTH // 4 - label_jump_search.get_width() // 2, HEIGHT // 2 + 10))

def draw_dividers():
    """Draw dividers between the squares."""
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 7)  # Vertical divider
    pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 7)  # Horizontal divider


def run_pathfinding(pathfinder, grid, path_found_flag, delay, color):
    """Thread function to run the pathfinding algorithm."""
    path = pathfinder.a_star()  # Replace this with the respective algorithm method
    if path:
        for position in path:
            with lock:  # Ensure grid update is thread-safe
                grid[position[0]][position[1]] = color
            pygame.time.delay(delay)
        path_found_flag[0] = True  # Mark the path as completed


# Initialize pathfinders
pathfinder_a_star = Pathfinding(grid_a_star, start, goal)
pathfinder_d_star = Pathfinding(grid_d_star, start, goal)
pathfinder_jump_search = Pathfinding(grid_jump_search, start, goal)  # Assuming Jump Search is implemented

path_found_a_star = [False]
path_found_d_star = [False]
path_found_jump_search = [False]

# Create threads for simultaneous execution
thread_a_star = threading.Thread(target=run_pathfinding, args=(pathfinder_a_star, grid_a_star, path_found_a_star, 50, 3))
thread_d_star = threading.Thread(target=run_pathfinding, args=(pathfinder_d_star, grid_d_star, path_found_d_star, 50, 4))
thread_jump_search = threading.Thread(target=run_pathfinding, args=(pathfinder_jump_search, grid_jump_search, path_found_jump_search, 50, 5))

# Start threads
thread_a_star.start()
thread_d_star.start()
thread_jump_search.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    with lock:
        draw_grid(grid_a_star, offset_x=0, offset_y=0)
        draw_grid(grid_d_star, offset_x=WIDTH // 2, offset_y=0)
        draw_grid(grid_jump_search, offset_x=0, offset_y=HEIGHT // 2)
        pygame.draw.rect(screen, BLACK, (WIDTH // 2, HEIGHT // 2, WIDTH // 2, HEIGHT // 2))

    draw_dividers()
    draw_labels()
    pygame.display.flip()

# Wait for threads to finish before quitting
thread_a_star.join()
thread_d_star.join()
thread_jump_search.join()
pygame.quit()
