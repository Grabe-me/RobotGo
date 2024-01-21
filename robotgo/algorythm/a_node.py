class Node:

    def __init__(self, x, y):
        """

        :param x: vertical distance (height)
        :param y: horizontal distance (width)
        """

        self.x = x
        self.y = y
        self.distance_fee = 0
        self.distance_from = 0
        self.distance_to = 0
        self.neighbors = []
        self.previous = None
        self.obstacle = False

    def add_neighbors(self, grid, columns, rows):

        neighbor_x = self.x
        neighbor_y = self.y

        if neighbor_x < columns - 1:
            self.neighbors.append(grid[neighbor_x + 1][neighbor_y])
        if neighbor_x > 0:
            self.neighbors.append(grid[neighbor_x - 1][neighbor_y])
        if neighbor_y < rows - 1:
            self.neighbors.append(grid[neighbor_x][neighbor_y + 1])
        if neighbor_y > 0:
            self.neighbors.append(grid[neighbor_x][neighbor_y - 1])
