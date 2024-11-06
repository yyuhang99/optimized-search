import pygame
from pathfinding import Pathfinding

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
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pathfinding Visualization")

# Initialize grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Define start and goal positions
start = (0, 0)
goal = (ROWS - 1, COLS - 1)
grid[start[0]][start[1]] = 1
grid[goal[0]][goal[1]] = 2

import random
for _ in range(150):  # Adjust number of obstacles
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
            elif grid[row][col] == 3: #Path
                color = YELLOW
            pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)  # Grid lines

# Initial draw
screen.fill(WHITE)
draw_grid()
pygame.display.flip()

running = True
path_found = False
pathfinder = Pathfinding(grid, start, goal)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the close button is clicked
            running = False  # Exit the loop, ending the program
    if not path_found:
        path = pathfinder.d_star() #TO BE REPLACED WITH ALGORITHM DETERMINER
        print(path)
        if path:
            for position in path:
                grid[position[0]][position[1]] = 3
                draw_grid()
                pygame.display.flip()
                pygame.time.delay(50)
            path_found = True
    # Redraw the screen each frame
    #screen.fill(WHITE)
    draw_grid()  # Draw the initial grid or update with each algorithm step if needed
    
    # Example placeholder: Run your pathfinding algorithm here and visualize the steps
    # path, explored = a_star_search(grid, start, goal)  # Example: replace with your algorithm
    # visualize_search(path, explored)
    
    pygame.display.flip()  # Update the display

pygame.quit()  # Properly close the Pygame window
