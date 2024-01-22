import pytest
from robotgo.algorythm import Node, AStar

GRID_MAP_1 = """
    0 1 0 1 0
    0 1 0 1 0
    0 0 0 1 0
    0 0 0 0 0
    """
START_1 = (0, 0)
END_1 = (3, 4)

GRID_MAP_2 = """
    0 1 0
    1 0 0
    1 0 1
    0 0 0
    """
START_2 = (0, 0)
END_2 = (3, 2)


def get_params(raw_grid_map: str):
    cols = raw_grid_map.strip().splitlines()
    rows = [col for col in cols[0] if col.isdigit()]
    grid_map = raw_grid_map.replace(" ", "").replace("\n", "")
    return len(cols), len(rows), grid_map


def get_params_with_grid(raw_grid_map: str):
    cols, rows, grid_map = get_params(raw_grid_map)
    grid = AStar.create_grid(cols, rows)
    grid = AStar.fill_grids(grid, cols, rows, grid_map)
    grid = AStar.get_neighbors(grid, cols, rows)
    return cols, rows, grid


@pytest.fixture
def example_grid(request):
    marker = request.node.get_closest_marker("fixt_data")
    data = marker.args
    raw_grid_map = data[0]
    cols, rows, grid = get_params_with_grid(raw_grid_map)
    if len(data) > 1:
        raw_grid_map, start_coords, end_coords = data
        start = Node(*start_coords)
        end = Node(*end_coords)
        a_star = AStar(cols, rows, start, end)
        return a_star, grid
    return grid
