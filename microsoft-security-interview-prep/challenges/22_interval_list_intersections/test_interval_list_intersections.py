import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = (
        "practice_interval_list_intersections"
        if use_practice
        else "solution_interval_list_intersections"
    )
    return importlib.import_module(module_name)


impl = _load_impl()


def test_classic_example():
    first = [[0, 2], [5, 10], [13, 23], [24, 25]]
    second = [[1, 5], [8, 12], [15, 24], [25, 26]]
    expected = [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]]
    assert impl.interval_intersections(first, second) == expected


def test_no_overlap():
    assert impl.interval_intersections([[1, 2]], [[3, 4]]) == []


def test_first_list_empty():
    assert impl.interval_intersections([], [[1, 5]]) == []


def test_second_list_empty():
    assert impl.interval_intersections([[1, 5]], []) == []


def test_both_lists_empty():
    assert impl.interval_intersections([], []) == []


def test_identical_intervals():
    assert impl.interval_intersections([[1, 5]], [[1, 5]]) == [[1, 5]]


def test_one_interval_fully_contains_another():
    assert impl.interval_intersections([[1, 10]], [[3, 5]]) == [[3, 5]]
