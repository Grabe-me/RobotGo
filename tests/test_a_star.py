import pytest
from robotgo.algorythm import Node, AStar


COLS_1 = 4
ROWS_1 = 5
MAP_1 = '01010010100001000000'

COLS_2 = 4
ROWS_2 = 3
MAP_2 = '010100101000'


@pytest.fixture
def example_grid():
    """
    0 1 0 1 0
    0 1 0 1 0
    0 0 0 1 0
    0 0 0 0 0
    :return:
    """
    start = Node(0, 0)
    end = Node(4, 4)
    a_star = AStar(COLS_1, ROWS_1, start, end)
    grid = AStar.create_grid(COLS_1, ROWS_1)
    grid = AStar.fill_grids(grid, COLS_1, ROWS_1, MAP_1)
    return a_star, grid


def test_create_grid():
    grid = AStar.create_grid(COLS_1, ROWS_1)
    assert len(grid) == COLS_1
    assert len(grid[0]) == ROWS_1


def test_fill_grids():
    """
    0 1 0
    1 0 0
    1 0 1
    0 0 0
    """
    grid = AStar.create_grid(COLS_2, ROWS_2)
    grid = AStar.fill_grids(grid, COLS_2, ROWS_2, MAP_2)
    assert grid[0][0].obstacle == False
    assert grid[0][1].obstacle == True
    assert grid[1][1].obstacle == False
    assert grid[2][2].obstacle == True
    assert grid[3][2].obstacle == False


def test_get_neighbors(example_grid):
    a_star, grid = example_grid
    grid = AStar.get_neighbors(grid, a_star.cols, a_star.rows)
    assert len(grid[0][0].neighbors) == 2  # Top-left corner
    assert len(grid[2][2].neighbors) == 4  # Center


def test_start_path(example_grid):
    a_star, grid = example_grid
    open_set = [grid[2][2]]
    grid = AStar.get_neighbors(grid, a_star.cols, a_star.rows)
    closed_set = []
    end = grid[3][4]
    open_set, closed_set, final_path = AStar.start_path(open_set, closed_set, end)
    assert len(open_set) == 3
    assert len(closed_set) == 1
    assert len(final_path) == 0
