import copy
import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_nearest_person_distance" if use_practice else "solution_nearest_person_distance"
    )
    return importlib.import_module(module_name)


impl = _load_impl()


def test_single_person_open_floor():
    building = [
        ["P", "E", "E"],
        ["E", "E", "E"],
    ]
    assert impl.nearest_person_distance(building) == [
        [0, 1, 2],
        [1, 2, 3],
    ]


def test_takes_minimum_across_multiple_people():
    building = [["P", "E", "E", "E", "P"]]
    assert impl.nearest_person_distance(building) == [[0, 1, 2, 1, 0]]


def test_locked_rooms_block_and_are_minus_one():
    building = [
        ["P", "L", "E"],
        ["E", "L", "E"],
        ["E", "E", "E"],
    ]
    assert impl.nearest_person_distance(building) == [
        [0, -1, 6],
        [1, -1, 5],
        [2, 3, 4],
    ]


def test_unreachable_empty_room_is_minus_one():
    building = [
        ["P", "L", "E"],
        ["L", "L", "E"],
    ]
    assert impl.nearest_person_distance(building) == [
        [0, -1, -1],
        [-1, -1, -1],
    ]


def test_no_people_at_all():
    building = [["E", "E"], ["L", "E"]]
    assert impl.nearest_person_distance(building) == [[-1, -1], [-1, -1]]


def test_non_square_grid():
    # Catches swapped row/col dimensions.
    building = [
        ["P", "E", "E", "E"],
        ["E", "E", "E", "E"],
    ]
    assert impl.nearest_person_distance(building) == [
        [0, 1, 2, 3],
        [1, 2, 3, 4],
    ]


def test_tall_grid():
    building = [["P"], ["E"], ["E"]]
    assert impl.nearest_person_distance(building) == [[0], [1], [2]]


def test_rows_are_independent_objects():
    # Catches `[[x] * cols] * rows` aliasing: writing one row must not write all rows.
    building = [
        ["P", "E"],
        ["E", "E"],
        ["E", "E"],
    ]
    result = impl.nearest_person_distance(building)
    assert result == [[0, 1], [1, 2], [2, 3]]
    assert result[0] is not result[1]


def test_does_not_mutate_input():
    building = [["P", "E"], ["L", "E"]]
    original = copy.deepcopy(building)
    impl.nearest_person_distance(building)
    assert building == original


def test_empty_grid():
    assert impl.nearest_person_distance([]) == []


def test_ragged_rows_raise():
    with pytest.raises(ValueError):
        impl.nearest_person_distance([["P", "E"], ["E"]])


def test_invalid_character_raises():
    with pytest.raises(ValueError):
        impl.nearest_person_distance([["P", "X"]])


def test_large_floor_many_people():
    # 400 x 400, every cell in column 0 is a person -> distance == column index.
    # One BFS per person (400 BFS runs over 160k cells) is far too slow here.
    n = 400
    building = [["P"] + ["E"] * (n - 1) for _ in range(n)]
    result = impl.nearest_person_distance(building)
    assert result[0] == list(range(n))
    assert result[n - 1][n - 1] == n - 1
