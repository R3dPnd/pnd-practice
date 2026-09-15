import importlib
import os


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_merge_intervals" if use_practice else "solution_merge_intervals"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_classic_example():
    assert impl.merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]) == [
        [1, 6],
        [8, 10],
        [15, 18],
    ]


def test_touching_intervals_merge():
    assert impl.merge_intervals([[1, 4], [4, 5]]) == [[1, 5]]


def test_empty_input():
    assert impl.merge_intervals([]) == []


def test_single_interval():
    assert impl.merge_intervals([[1, 2]]) == [[1, 2]]


def test_no_overlaps_stay_separate():
    assert impl.merge_intervals([[1, 2], [4, 5], [7, 8]]) == [[1, 2], [4, 5], [7, 8]]


def test_unsorted_input_gets_sorted():
    assert impl.merge_intervals([[5, 6], [1, 2], [3, 4]]) == [[1, 2], [3, 4], [5, 6]]


def test_fully_nested_interval():
    assert impl.merge_intervals([[1, 10], [2, 3], [4, 5]]) == [[1, 10]]


def test_does_not_mutate_input():
    original = [[1, 3], [2, 6]]
    snapshot = [list(iv) for iv in original]
    impl.merge_intervals(original)
    assert original == snapshot
