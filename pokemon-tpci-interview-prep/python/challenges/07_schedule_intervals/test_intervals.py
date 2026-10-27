import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_intervals" if use_practice else "solution_intervals")


impl = _load_impl()


def test_merge():
    data = [(8, 10), (1, 3), (2, 6), (15, 18), (6, 7)]
    assert impl.merge(data) == [(1, 7), (8, 10), (15, 18)]
    assert data[0] == (8, 10), "input mutated"
    assert impl.merge([]) == []
    assert impl.merge([(1, 10), (2, 3)]) == [(1, 10)]


def test_has_conflict():
    assert not impl.has_conflict([(0, 30), (30, 60), (60, 90)])
    assert impl.has_conflict([(60, 90), (0, 30), (20, 40)])


@pytest.mark.parametrize("data,want", [
    ([], 0),
    ([(0, 30), (5, 10), (15, 20)], 2),
    ([(0, 10), (10, 20)], 1),
    ([(1, 5), (2, 6), (3, 7), (6, 8)], 3),
])
def test_min_tables(data, want):
    assert impl.min_tables(data) == want
