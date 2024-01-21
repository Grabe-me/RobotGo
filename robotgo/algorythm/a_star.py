from robotgo.algorythm import Node


class AStar:
    def __init__(self, cols, rows, start, end):
        self.cols = cols
        self.rows = rows
        self.start = start
        self.end = end
        self.obstacle_ratio = False
        self.obstacle_list = False

    @staticmethod
    def clean_open_set(open_set: list, current_node):
        try:
            open_set.remove(current_node)
        except ValueError:
            pass
        finally:
            return open_set

    @staticmethod
    def heuristic_score(current_node, end) -> int:
        """Heuristic distance to end point"""
        return abs(current_node.x - end.x) + abs(current_node.y - end.y)

    @staticmethod
    def create_grid(cols: int, rows: int) -> list[list]:
        """
        Creating empty matrix with lists (cols * rows)
        N=cols
        M=rows
        """
        return [[[] for _ in range(rows)] for _ in range(cols)]

    @staticmethod
    def fill_grids(
        grid: list[list[Node]], cols: int, rows: int, obstacle_map: str
    ) -> list[list[Node]]:
        """
        Filling grid with Node items
        N=cols=i
        M=rows=j
        obstacle_map='01010010100001000000'
        """

        for i in range(cols):
            for j in range(rows):
                grid[i][j] = Node(i, j)
                if int(obstacle_map[i * rows + j]):
                    grid[i][j].obstacle = True

        return grid

    @staticmethod
    def get_neighbors(grid, cols, rows) -> list[list[Node]]:
        """Adding neighbours Nodes for each Node"""
        for i in range(cols):
            for j in range(rows):
                grid[i][j].add_neighbors(grid, cols, rows)
        return grid

    @staticmethod
    def start_path(open_set: list, closed_set: list, end: Node):
        best_way = 0
        for i in range(len(open_set)):
            if open_set[i].distance_fee < open_set[best_way].distance_fee:
                best_way = i

        current_node = open_set[best_way]
        final_path = []

        if current_node == end:
            temp_node = current_node
            final_path.append(current_node)
            while temp_node.previous:
                final_path.append(temp_node.previous)
                temp_node = temp_node.previous

        open_set = AStar.clean_open_set(open_set, current_node)
        closed_set.append(current_node)
        neighbors = current_node.neighbors
        for neighbor in neighbors:
            if (neighbor in closed_set) or (neighbor.obstacle == True):
                continue
            else:
                temp_distance_from = current_node.distance_from + 1
                control_flag = 0
                for k in range(len(open_set)):
                    if neighbor.x == open_set[k].x and neighbor.y == open_set[k].y:
                        if temp_distance_from < open_set[k].distance_from:
                            open_set[k].distance_from = temp_distance_from
                            open_set[k].distance_to = AStar.heuristic_score(
                                open_set[k], end
                            )
                            open_set[k].distance_fee = (
                                open_set[k].distance_from + open_set[k].distance_to
                            )
                            open_set[k].previous = current_node
                        control_flag = 1
                if control_flag != 1:
                    neighbor.distance_from = temp_distance_from
                    neighbor.distance_to = AStar.heuristic_score(neighbor, end)
                    neighbor.distance_fee = (
                        neighbor.distance_from + neighbor.distance_to
                    )
                    neighbor.previous = current_node
                    open_set.append(neighbor)

        return open_set, closed_set, final_path
