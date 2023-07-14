import pygame
from collections import deque

# Define the maze
maze = [
    ["S", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    [" ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "E"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
]

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Define the maze size and cell size
MAZE_SIZE = 11
CELL_SIZE = 40

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((MAZE_SIZE * CELL_SIZE, MAZE_SIZE * CELL_SIZE))
pygame.display.set_caption("Maze Solver")

# Clock for controlling the frame rate
clock = pygame.time.Clock()


def draw_maze():
    """Draw the maze on the screen"""
    screen.fill(WHITE)
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = BLACK
            if maze[row][col] == "S":
                color = GREEN
            elif maze[row][col] == "E":
                color = RED
            elif maze[row][col] == "#":
                color = BLUE

            pygame.draw.rect(
                screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )


def is_valid_move(row, col):
    """Check if a move is valid (within bounds and not a wall)"""
    if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != "#":
        return True
    return False


def bfs_solver():
    # Start and end positions
    start = None
    end = None

    # Find the start and end positions
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == "S":
                start = (row, col)
            elif maze[row][col] == "E":
                end = (row, col)

    # Queue for BFS
    queue = deque([(start, [])])

    # Visited set to keep track of visited cells
    visited = set([start])

    while queue:
        current, path = queue.popleft()
        row, col = current

        # Check if reached the end point
        if current == end:
            return path + [current]

        # Explore all possible moves
        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dr, col + dc

            if is_valid_move(new_row, new_col) and (new_row, new_col) not in visited:
                queue.append(((new_row, new_col), path + [current]))
                visited.add((new_row, new_col))

                # Update the maze with the visited cell for visualization
                maze[new_row][new_col] = "#"

                # Draw the maze with the updated cell
                draw_maze()
                pygame.display.flip()
                pygame.time.delay(100)  # Delay to visualize the solving process

    # If no path is found
    return None


# Draw the initial maze
draw_maze()
pygame.display.flip()

# Solve the maze
solution = bfs_solver()

# Update the maze with the solution path
if solution:
    for row, col in solution:
        maze[row][col] = "#"

# Draw the final maze with the solution path
draw_maze()
pygame.display.flip()

# Keep the Pygame window open until closed by the user
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

# Quit Pygame
pygame.quit()
