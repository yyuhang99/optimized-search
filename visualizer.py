import pygame
import random
from pathfinding import Pathfinding
import threading

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 600
ROWS, COLS = 30, 30
CELL_SIZE = HEIGHT // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create the Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualization: A* vs D*")

# Initialize grids
grid_a_star = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid_d_star = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Define start and goal points
start = (0, 0)
goal = (ROWS - 1, COLS - 1)

# Place obstacles
for _ in range(150):
    x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    if (x, y) != start and (x, y) != goal:
        grid_a_star[x][y] = -1
        grid_d_star[x][y] = -1

# Mark start and goal points
grid_a_star[start[0]][start[1]] = 1
grid_a_star[goal[0]][goal[1]] = 2
grid_d_star[start[0]][start[1]] = 1
grid_d_star[goal[0]][goal[1]] = 2

# Lock for thread synchronization
lock = threading.Lock()


def draw_grid(grid, offset_x):
    """Draw the grid on the screen."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid[row][col] == -1:  # Obstacle
                color = BLACK
            elif grid[row][col] == 1:  # Start
                color = GREEN
            elif grid[row][col] == 2:  # Goal
                color = RED
            elif grid[row][col] == 3:  # Path
                color = YELLOW
            pygame.draw.rect(
                screen,
                color,
                (offset_x + col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )
            pygame.draw.rect(
                screen,
                BLUE,
                (offset_x + col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1,
            )  # Grid lines


def draw_divider():
    """Draw a divider between the two visualizations."""
    pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 7)


def draw_labels():
    """Draw labels for A* and D* visualizations."""
    font = pygame.font.Font(None, 36)
    label_a_star = font.render("A* Algorithm", True, BLACK)
    label_d_star = font.render("D* Algorithm", True, BLACK)
    screen.blit(label_a_star, (WIDTH // 4 - label_a_star.get_width() // 2, 10))
    screen.blit(label_d_star, (3 * WIDTH // 4 - label_d_star.get_width() // 2, 10))


def run_pathfinding(pathfinder, grid, path_found_flag, delay):
    """Thread function to run the pathfinding algorithm."""
    path = pathfinder.a_star()  # Use the appropriate algorithm here
    if path:
        for position in path:
            with lock:  # Ensure grid update is thread-safe
                grid[position[0]][position[1]] = 3
            pygame.time.delay(delay)
        path_found_flag[0] = True  # Mark the path as completed


# Initialize pathfinders
pathfinder_a_star = Pathfinding(grid_a_star, start, goal)
pathfinder_d_star = Pathfinding(grid_d_star, start, goal)

# Flags to check if paths are found
path_found_a_star = [False]
path_found_d_star = [False]

# Create threads for simultaneous execution
thread_a_star = threading.Thread(target=run_pathfinding, args=(pathfinder_a_star, grid_a_star, path_found_a_star, 50))
thread_d_star = threading.Thread(target=run_pathfinding, args=(pathfinder_d_star, grid_d_star, path_found_d_star, 50))

# Start threads
thread_a_star.start()
thread_d_star.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw UI
    screen.fill(WHITE)
    with lock:  # Ensure drawing is thread-safe
        draw_grid(grid_a_star, offset_x=0)
        draw_grid(grid_d_star, offset_x=WIDTH // 2)
    draw_divider()
    draw_labels()
    pygame.display.flip()

# Wait for threads to finish before quitting
thread_a_star.join()
thread_d_star.join()
pygame.quit()
