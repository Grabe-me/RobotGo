from robotgo.algorythm import AStar, Node

COLS = 4
ROWS = 5
MAP = "01010010100001000000"

START_COORD = (0, 0)
END_COORD = (3, 4)


def get_grid(cols: int, rows: int, obstacle_map: str) -> list[list[Node]]:
    grid = AStar.create_grid(cols, rows)
    grid = AStar.fill_grids(grid, cols, rows, obstacle_map)
    grid = AStar.get_neighbors(grid, cols, rows)
    return grid


def algorythm(
    start_coords: tuple[int], end_coords: tuple[int], grid: list[list[Node]]
) -> list[Node]:
    open_set: list[Node] = []
    closed_set: list[Node] = []
    final_path: list[Node] = []
    open_set.append(grid[start_coords[0]][start_coords[1]])  # type: ignore
    end = grid[end_coords[0]][end_coords[1]]  # type: ignore
    while len(open_set) > 0:
        open_set, closed_set, final_path = AStar.start_path(open_set, closed_set, end)
        if len(final_path) > 0:
            final_path.reverse()
            break

    return final_path
