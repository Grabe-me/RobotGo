import pytest

from robotgo.algorythm import AStar, algorythm

COLS = 4
ROWS = 5
MAP = '01010010100001000000'
START_COORD = (0, 0)
END_COORD = (3, 4)


@pytest.fixture
def example_grid():
    grid = AStar.create_grid(COLS, ROWS)
    grid = AStar.fill_grids(grid, COLS, ROWS, MAP)
    grid = AStar.get_neighbors(grid, COLS, ROWS)
    return grid


def test_main():
    final_path = algorythm(COLS, ROWS, START_COORD, END_COORD, MAP)
    assert len(final_path) > 0
    assert final_path[0].x == START_COORD[0]
    assert final_path[0].y == START_COORD[1]
    assert final_path[-1].x == END_COORD[0]
    assert final_path[-1].y == END_COORD[1]


def test_main_invalid_coords():
    with pytest.raises(IndexError):
        algorythm(COLS, ROWS, (5, 0), END_COORD, MAP)
