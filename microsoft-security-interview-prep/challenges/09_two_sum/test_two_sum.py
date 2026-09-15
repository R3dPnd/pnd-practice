import importlib
import os

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_two_sum" if use_practice else "solution_two_sum"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_basic_case():
    assert sorted(impl.two_sum([2, 7, 11, 15], 9)) == [0, 1]


def test_pair_not_at_start():
    nums = [3, 2, 4]
    a, b = impl.two_sum(nums, 6)
    assert a != b
    assert nums[a] + nums[b] == 6


def test_duplicate_values_use_different_indices():
    result = impl.two_sum([3, 3], 6)
    assert sorted(result) == [0, 1]


def test_handles_negative_numbers():
    nums = [-3, 4, 3, 90]
    result = impl.two_sum(nums, 0)
    a, b = result
    assert nums[a] + nums[b] == 0
    assert a != b


def test_raises_when_no_solution():
    with pytest.raises(ValueError):
        impl.two_sum([1, 2, 3], 100)
