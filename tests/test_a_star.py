import pytest
from robotgo.algorythm import AStar
from tests.conftest import GRID_MAP_1, START_1, END_1, GRID_MAP_2


@pytest.mark.parametrize("cols, rows", [(4, 5), (9, 7)])
def test_create_grid(cols, rows):
    grid = AStar.create_grid(cols, rows)
    assert len(grid) == cols
    assert len(grid[0]) == rows


@pytest.mark.fixt_data(GRID_MAP_2)
@pytest.mark.parametrize(
    "x, y, res",
    [(0, 0, False), (0, 1, True), (1, 1, False), (2, 2, True), (3, 2, False)],
)
def test_fill_grids(x: int, y: int, res: bool, example_grid):
    assert example_grid[x][y].obstacle == res


@pytest.mark.parametrize(
    "x, y, res", [(0, 0, 2), (2, 2, 4)]  # Top-left corner  # Center
)
@pytest.mark.fixt_data(GRID_MAP_1, START_1, END_1)
def test_get_neighbors(example_grid, x, y, res):
    a_star, grid = example_grid
    assert len(grid[x][y].neighbors) == res


@pytest.mark.fixt_data(GRID_MAP_1, START_1, END_1)
def test_start_path(example_grid):
    a_star, grid = example_grid
    open_set = [grid[2][2]]
    closed_set = []
    open_set, closed_set, final_path = AStar.start_path(
        open_set, closed_set, a_star.end
    )
    assert len(open_set) == 3
    assert len(closed_set) == 1
    assert len(final_path) == 0
