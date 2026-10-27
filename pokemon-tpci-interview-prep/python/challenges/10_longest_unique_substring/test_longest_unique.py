import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    return importlib.import_module("practice_longest_unique" if use_practice else "solution_longest_unique")


impl = _load_impl()


@pytest.mark.parametrize("s,want", [
    ("", 0), ("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("abba", 2), ("ポケモン", 4), ("ピカピカ", 2),
])
def test_longest_unique(s, want):
    assert impl.longest_unique(s) == want
