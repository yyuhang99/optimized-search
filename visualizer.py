import pygame
import random
from pathfinding import Pathfinding  # A* Implementation
from jumpstart import JumpStart

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 30, 30  # Number of rows and columns in the grid
CELL_SIZE = WIDTH // COLS

# Colors for visualization
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)  # A* Path Color
ORANGE = (255, 165, 0)  # JPS Path Color
BLUE = (0, 0, 255)      # Grid lines

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* and Jump Point Search Visualization")

# Initialize grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Define start and goal positions
start = (0, 0)
goal = (ROWS - 1, COLS - 1)
grid[start[0]][start[1]] = 1
grid[goal[0]][goal[1]] = 2

# Add random obstacles
for _ in range(150):  # Adjust the number of obstacles
    x, y = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    if (x, y) != start and (x, y) != goal:
        grid[x][y] = -1

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
            elif grid[row][col] == 3:  # A* Path
                color = YELLOW
            elif grid[row][col] == 4:  # JPS Path
                color = ORANGE
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Grid lines

# Initial draw
screen.fill(WHITE)
draw_grid()
pygame.display.flip()

running = True
a_star_path_found = False
jps_path_found = False

# Initialize A* and Jump Point Search
a_star = Pathfinding(grid, start, goal)
jps = JumpStart(grid, start, goal)

# Main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not a_star_path_found:
        # Run A* Algorithm
        a_star_path = a_star.a_star()
        if a_star_path:
            for position in a_star_path:
                grid[position[0]][position[1]] = 3  # Mark A* Path
                draw_grid()
                pygame.display.flip()
                pygame.time.delay(50)
            a_star_path_found = True

    if not jps_path_found:
        # Run Jump Point Search
        jps_path = jps.jump_point_search()
        if jps_path:
            for position in jps_path:
                grid[position[0]][position[1]] = 4  # Mark JPS Path
                draw_grid()
                pygame.display.flip()
                pygame.time.delay(50)
            jps_path_found = True

    # Redraw the grid
    draw_grid()
    pygame.display.flip()

pygame.quit()
