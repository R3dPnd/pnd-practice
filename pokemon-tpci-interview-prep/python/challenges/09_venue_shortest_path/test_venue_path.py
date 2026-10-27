import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_venue_path" if use_practice else "solution_venue_path")


impl = _load_impl()


@pytest.mark.parametrize("grid,want", [
    (["S..E"], 3),
    (["S.#.", "..#E", "...."], 6),
    (["S#.", "##E"], -1),
    (["S#E", "..."], 4),
    (["S.."], -1),
])
def test_shortest_path(grid, want):
    assert impl.shortest_path(grid) == want
