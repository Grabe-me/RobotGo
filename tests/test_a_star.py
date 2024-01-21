import pytest

from robotgo.algorythm import Node, AStar


@pytest.fixture
def example_grid():
    """
    0 1 0 1 0
    0 1 0 1 0
    0 0 0 1 0
    0 0 0 0 0
    :return:
    """
    cols = 4
    rows = 5
    obstacle_map = '01010010100001000000'
    start = Node(0, 0)
    end = Node(4, 4)
    a_star = AStar(cols, rows, start, end)
    grid = AStar.create_grid(cols, rows)
    grid = AStar.fill_grids(grid, cols, rows, obstacle_map)
    return a_star, grid


def test_create_grid():
    cols = 4
    rows = 3
    grid = AStar.create_grid(cols, rows)
    assert len(grid) == rows
    assert len(grid[0]) == cols


def test_fill_grids():
    cols = 4
    rows = 3
    obstacle_map = '010100101000'
    """
    0 1 0
    1 0 0
    1 0 1
    0 0 0
    """
    grid = AStar.create_grid(cols, rows)
    grid = AStar.fill_grids(grid, cols, rows, obstacle_map)
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
