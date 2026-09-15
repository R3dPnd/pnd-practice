import copy
import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_number_of_islands" if use_practice else "solution_number_of_islands"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_classic_example():
    grid = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert impl.num_islands(grid) == 3


def test_empty_grid():
    assert impl.num_islands([]) == 0
    assert impl.num_islands([[]]) == 0


def test_all_water():
    grid = [["0", "0"], ["0", "0"]]
    assert impl.num_islands(grid) == 0


def test_all_land_is_one_island():
    grid = [["1", "1"], ["1", "1"]]
    assert impl.num_islands(grid) == 1


def test_diagonal_touch_is_not_connected():
    grid = [
        ["1", "0"],
        ["0", "1"],
    ]
    assert impl.num_islands(grid) == 2


def test_single_cell_island():
    grid = [["1"]]
    assert impl.num_islands(grid) == 1


def test_does_not_mutate_input_grid():
    grid = [
        ["1", "1", "0"],
        ["0", "0", "1"],
    ]
    snapshot = copy.deepcopy(grid)
    impl.num_islands(grid)
    assert grid == snapshot
