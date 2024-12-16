import pygame
import random
import time  # For measuring runtime
from pathfinding import Pathfinding  # A* Implementation
from jumpstart import JumpStart

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 30, 30  # Number of rows and columns in the grid
CELL_SIZE = min(WIDTH // 2 // COLS, HEIGHT // 2 // ROWS) - 1

# Colors for visualization
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # A* Path Color
ORANGE = (255, 165, 0)  # JPS Path Color
BLUE = (0, 0, 255)      # D* Path Color
GRAY = (128, 128, 128)  # Grid lines

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualization with Runtime Stats")

# Initialize grids
grid_a_star = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid_jps = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid_d_star = [[0 for _ in range(COLS)] for _ in range(ROWS)]
grid_combined = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Define start and goal positions
start = (0, 0)
goal = (ROWS - 1, COLS - 1)

# Populate grids with obstacles
for grid in [grid_a_star, grid_jps, grid_d_star, grid_combined]:
    for _ in range(150):
        x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (x, y) != start and (x, y) != goal:
            grid[x][y] = -1
    grid[start[0]][start[1]] = 1  # Start point
    grid[goal[0]][goal[1]] = 2    # Goal point


def draw_grid(grid, offset_x, offset_y):
    """Draw the grid in its designated area."""
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE
            if grid[row][col] == -1:  # Obstacle
                color = BLACK
            elif grid[row][col] == 1:  # Start
                color = GREEN
            elif grid[row][col] == 2:  # Goal
                color = RED
            elif grid[row][col] == 3:  # A* Path
                color = YELLOW
            elif grid[row][col] == 4:  # JPS Path
                color = ORANGE
            elif grid[row][col] == 5:  # D* Path
                color = BLUE

            pygame.draw.rect(
                screen,
                color,
                (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
            pygame.draw.rect(
                screen,
                GRAY,
                (offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                1
            )


def draw_runtime(runtime, offset_x, offset_y, label):
    """Display runtime statistics for each algorithm."""
    font = pygame.font.Font(None, 24)
    text = f"{label} Runtime: {runtime:.3f} ms"
    rendered_text = font.render(text, True, BLACK)
    screen.blit(rendered_text, (offset_x + 10, offset_y + ROWS * CELL_SIZE + 5))


# Initialize pathfinding objects
a_star = Pathfinding(grid_a_star, start, goal)
jps = JumpStart(grid_jps, start, goal)
d_star = Pathfinding(grid_d_star, start, goal)

# Flags for completion
a_star_complete = False
jps_complete = False
d_star_complete = False

# Runtime tracking
a_star_runtime = 0
jps_runtime = 0
d_star_runtime = 0

running = True

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Run A* algorithm
    if not a_star_complete:
        start_time = time.time()
        a_star_path = a_star.a_star()
        end_time = time.time()
        a_star_runtime = (end_time - start_time) * 1000  # Convert to milliseconds
        if a_star_path:
            for position in a_star_path:
                grid_a_star[position[0]][position[1]] = 3  # Mark A* Path
                draw_grid(grid_a_star, 0, 0)
                pygame.display.flip()
                pygame.time.delay(50)
            a_star_complete = True

    # Run Jump Point Search
    if not jps_complete:
        start_time = time.time()
        jps_path = jps.jump_point_search()
        end_time = time.time()
        jps_runtime = (end_time - start_time) * 1000  # Convert to milliseconds
        if jps_path:
            for position in jps_path:
                grid_jps[position[0]][position[1]] = 4  # Mark JPS Path
                draw_grid(grid_jps, WIDTH // 2, 0)
                pygame.display.flip()
                pygame.time.delay(50)
            jps_complete = True

    # Run D* algorithm
    if not d_star_complete:
        start_time = time.time()
        d_star_path = d_star.d_star()
        end_time = time.time()
        d_star_runtime = (end_time - start_time) * 1000  # Convert to milliseconds
        if d_star_path:
            for position in d_star_path:
                grid_d_star[position[0]][position[1]] = 5  # Mark D* Path
                draw_grid(grid_d_star, 0, HEIGHT // 2)
                pygame.display.flip()
                pygame.time.delay(50)
            d_star_complete = True

    # Update display
    screen.fill(WHITE)
    draw_grid(grid_a_star, 0, 0)          # Top-left quadrant
    draw_grid(grid_jps, WIDTH // 2, 0)   # Top-right quadrant
    draw_grid(grid_d_star, 0, HEIGHT // 2)  # Bottom-left quadrant
    draw_grid(grid_combined, WIDTH // 2, HEIGHT // 2)  # Bottom-right quadrant

    # Draw runtime statistics
    draw_runtime(a_star_runtime, 0, 0, "A*")
    draw_runtime(jps_runtime, WIDTH // 2, 0, "JPS")
    draw_runtime(d_star_runtime, 0, HEIGHT // 2, "D*")

    pygame.display.flip()

pygame.quit()
