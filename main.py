from robotgo.algorythm import AStar, Node

COLS = 4
ROWS = 5
MAP = '01010010100001000000'

START_COORD = (0, 0)
END_COORD = (3, 4)


def main(
    cols: int,
    rows: int,
    start_coords: tuple,
    end_coords: tuple,
    obstacle_map: str
):
    grid = AStar.create_grid(cols, rows)
    grid = AStar.fill_grids(grid, cols, rows, obstacle_map)
    grid = AStar.get_neighbors(grid, cols, rows)
    open_set = []
    closed_set = []
    final_path = []
    open_set.append(grid[start_coords[0]][start_coords[1]])
    end = grid[end_coords[0]][end_coords[1]]
    while len(open_set) > 0:
        open_set, closed_set, final_path = AStar.start_path(open_set, closed_set, end)
        if len(final_path) > 0:
            final_path.reverse()
            break

    return final_path


if __name__ == "__main__":
    g = main(COLS, ROWS, START_COORD, END_COORD, MAP)
    for i in g:
        print(f"{i.x}, {i.y}")