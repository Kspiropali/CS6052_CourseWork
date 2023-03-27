import heapq
import time

import pygame
import os

os.environ["SDL_VIDEODRIVER"] = "x11"

""" Define the colors we will use in RGB format"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

""" Set the height and width of the screen"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

""" This sets the margin between each cell"""
MARGIN = 1

""" Set the number of rows and columns on the board"""
ROWS = 5
COLS = 6

""" Define the maze"""
MAZE = [[0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 0],
        [0, 0, 0, 0, 1, 0]]

""" Define the starting and ending positions"""
START = (0, 0)
END = (4, 5)


def heuristic(a, b):
    """Calculate the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(current_node):
    """Return the neighboring nodes of the current node."""
    row, col = current_node
    neighbors = []
    if row > 0 and not MAZE[row - 1][col]:
        neighbors.append((row - 1, col))
    if row < ROWS - 1 and not MAZE[row + 1][col]:
        neighbors.append((row + 1, col))
    if col > 0 and not MAZE[row][col - 1]:
        neighbors.append((row, col - 1))
    if col < COLS - 1 and not MAZE[row][col + 1]:
        neighbors.append((row, col + 1))
    return neighbors


def get_cost(__current_node, __neighbor):
    """Return the cost of moving from the current node to a neighbor."""
    """In our case, the cost of 2 adjacent paths will always be 1"""
    return 1


def uniform_cost_search(start, end):
    """Find the shortest path from the start node to the end node using uniform cost search."""
    frontier = [(0, start)]
    came_from = {}
    cost_so_far = {start: 0}

    while frontier:
        _, current_node = heapq.heappop(frontier)

        if current_node == end:
            break

        for neighbor in get_neighbors(current_node):
            new_cost = cost_so_far[current_node] + get_cost(current_node, neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current_node

    path = []
    current_node = end
    while current_node != start:
        path.append(current_node)
        current_node = came_from[current_node]
    path.append(start)
    path.reverse()

    return path


def draw_board(screen, path):
    """Draw the maze on the screen."""
    """ Clear the screen"""
    screen.fill(BLACK)

    """ Draw the cells"""
    for row in range(ROWS):
        for col in range(COLS):
            if MAZE[row][col]:
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(screen, color, [(MARGIN + SCREEN_WIDTH // COLS) * col + MARGIN,
                                             (MARGIN + SCREEN_HEIGHT // ROWS) * row + MARGIN,
                                             SCREEN_WIDTH // COLS,
                                             SCREEN_HEIGHT // ROWS])
            """ Draw the start and end positions"""
            pygame.draw.circle(screen, GREEN, [(MARGIN + SCREEN_WIDTH // COLS) * START[1] + SCREEN_WIDTH // (COLS * 2),
                                               (MARGIN + SCREEN_HEIGHT // ROWS) * START[0] + SCREEN_HEIGHT // (
                                                       ROWS * 2)],
                               min(SCREEN_WIDTH // COLS, SCREEN_HEIGHT // ROWS) // 3)

    """Draw the path"""
    if path:
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            pygame.draw.line(screen, GREEN,
                             [(MARGIN + SCREEN_WIDTH // COLS) * current_node[1] + SCREEN_WIDTH // (COLS * 2),
                              (MARGIN + SCREEN_HEIGHT // ROWS) * current_node[0] + SCREEN_HEIGHT // (ROWS * 2)],
                             [(MARGIN + SCREEN_WIDTH // COLS) * next_node[1] + SCREEN_WIDTH // (COLS * 2),
                              (MARGIN + SCREEN_HEIGHT // ROWS) * next_node[0] + SCREEN_HEIGHT // (ROWS * 2)], 5)
            pygame.display.flip()
            time.sleep(0.5)

    """Draw the end position"""
    pygame.draw.circle(screen, PURPLE, [(MARGIN + SCREEN_WIDTH // COLS) * END[1] + SCREEN_WIDTH // (COLS * 2),
                                     (MARGIN + SCREEN_HEIGHT // ROWS) * END[0] + SCREEN_HEIGHT // (ROWS * 2)],
                       min(SCREEN_WIDTH // COLS, SCREEN_HEIGHT // ROWS) // 3)
    """ Update the screen"""
    pygame.display.flip()


def main():
    """ Initialize Pygame"""
    pygame.init()
    """ Set the size of the screen"""
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    """ Set the caption of the screen"""
    pygame.display.set_caption("Maze")

    """ Set the clock"""
    clock = pygame.time.Clock()

    """ Run the uniform cost search algorithm"""
    path = uniform_cost_search(START, END)

    """Draw the board"""
    draw_board(screen, path)
    # add a big circle to the end position

    # add a big circle to the end position

    """ Wait for the user to close the window"""
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        """ Set the FPS"""
        clock.tick(60)

    """ Close Pygame"""
    pygame.quit()


if __name__ == "__main__":
    main()
