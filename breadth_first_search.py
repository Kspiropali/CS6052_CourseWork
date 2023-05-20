import os
import sys
import time

import pygame

# check if using linux or not
if os.name == "posix":
    """ if using linux, set the display driver to x11 """
    os.environ["SDL_VIDEODRIVER"] = "x11"

# Define the maze as a 2D array of nodes, where 0 = empty, 1 = obstacle
maze = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0],
]

# Define the starting and ending nodes
start_node = (0, 0)
end_node = (4, 5)

# Define the colors for the maze, nodes, and path
NODE_COLOR = (255, 255, 255)  # White
OBSTACLE_COLOR = (255, 0, 0)  # Red
START_COLOR = (0, 255, 0)  # Green
END_COLOR = (0, 0, 255)  # Blue
PATH_COLOR = (255, 255, 0)  # Yellow

# Define the width and height of each node in pixels
NODE_SIZE = 150
TILE_SIZE = NODE_SIZE

# Define the width and height of the window in pixels
WINDOW_WIDTH = NODE_SIZE * len(maze[0])
WINDOW_HEIGHT = NODE_SIZE * len(maze)

# Initialize Pygame
pygame.init()

# Create the Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Solver")


# Define a function to draw the maze on the screen
def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            rect = pygame.Rect(col * NODE_SIZE, row * NODE_SIZE, NODE_SIZE, NODE_SIZE)
            if maze[row][col] == 1:
                pygame.draw.rect(screen, OBSTACLE_COLOR, rect)
            else:
                pygame.draw.rect(screen, NODE_COLOR, rect)
            # Draw grid lines
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)


# Define a function to draw a node on the screen
def draw_node(color, node):
    rect = pygame.Rect(node[1] * NODE_SIZE, node[0] * NODE_SIZE, NODE_SIZE, NODE_SIZE)
    pygame.draw.rect(screen, color, rect)


# Define the breadth-first search algorithm
def bfs(start, end, maze):
    queue = [(start, [start])]
    visited = set()

    while queue:
        curr, path = queue.pop(0)
        x, y = curr

        # Check if the current node is the end node
        if curr == end:
            print("Found path:", path)
            visualize_path(path, maze)
            return path

        # Mark current node as visited
        visited.add(curr)

        # Visualize current search path
        visualize_path(path, maze)
        # draw the last node if found

        draw_node(END_COLOR, curr)
        pygame.display.update()

        # Explore neighboring nodes
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            neighbor = (x + dx, y + dy)

            # Check if neighbor is a valid node
            if 0 <= neighbor[0] < len(maze) and 0 <= neighbor[1] < len(maze[0]) and maze[neighbor[0]][
                neighbor[1]] != 1 and neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    print("No path found")
    return None


def visualize_path(path, maze):
    draw_maze()
    for node in path:
        pygame.display.update()

    for i in range(len(path) - 1):
        curr = path[i]
        next_node = path[i + 1]
        curr_x, curr_y = curr
        next_x, next_y = next_node
        pygame.draw.line(screen, (255, 0, 255),
                         (curr_y * TILE_SIZE + TILE_SIZE // 2, curr_x * TILE_SIZE + TILE_SIZE // 2),
                         (next_y * TILE_SIZE + TILE_SIZE // 2, next_x * TILE_SIZE + TILE_SIZE // 2), 4)

        # draw the end node
        if i == len(path) - 2:
            draw_node(END_COLOR, next_node)
        pygame.display.update()

    time.sleep(0.07)


def get_path(end_node):
    # Create an empty list to store the nodes in the path
    path = []

    # Starting from the end node, follow the parent nodes backwards until we reach the start node
    node = end_node
    while node is not None:
        # Add the current node to the path
        path.append(node)

        # Move to the parent node
        node = node.parent

    # Reverse the order of the path to go from start to end
    path.reverse()

    # Return the path as a list of coordinates
    return [(node.x, node.y) for node in path]


# Initialize maze, start, and end nodes
# Call BFS algorithm to find path
path = bfs(start_node, end_node, maze)
# draw the path from start to end node via the path list
for node in path:
    # draw initial paths
    draw_node(PATH_COLOR, node)
    # draw a line path

    pygame.display.update()
    time.sleep(0.3)
# Keep Pygame window open until closed by user
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
