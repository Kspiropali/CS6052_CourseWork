import heapq

"""The number of rows and columns on the board"""
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
            new_cost = cost_so_far[current_node] + get_cost(current_node, neighbor)  # get cost of moving from
            # current node to neighbor
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost  # cost_so_far[(2,3): cost_so_far() + 1]
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


def main():
    """ Run the uniform cost search algorithm"""
    path = uniform_cost_search(START, END)

    # prints a visual representation of the maze in the terminal to help visualize the path
    for row in range(ROWS):
        for col in range(COLS):
            if (row, col) in path:
                print("P", end=" ")
            elif MAZE[row][col] == 1:
                print("X", end=" ")
            else:
                print("_", end=" ")
        print()

    print(path)


if __name__ == "__main__":
    main()
