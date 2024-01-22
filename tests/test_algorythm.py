import pytest
from robotgo.algorythm import algorythm
from tests.conftest import GRID_MAP_1, START_1, END_1


@pytest.mark.fixt_data(GRID_MAP_1, START_1, END_1)
def test_main(example_grid):
    start = example_grid[0].start
    end = example_grid[0].end
    print(len(example_grid[1]))
    print(len(example_grid[1][0]))
    final_path = algorythm((start.x, start.y), (end.x, end.y), example_grid[1])
    assert len(final_path) > 0
    assert final_path[0].x == start.x
    assert final_path[0].y == start.y
    assert final_path[-1].x == end.x
    assert final_path[-1].y == end.y


@pytest.mark.fixt_data(GRID_MAP_1, START_1, END_1)
def test_main_invalid_coords(example_grid):
    end = example_grid[0].end
    with pytest.raises(IndexError):
        algorythm((5, 0), (end.x, end.y), example_grid[1])
