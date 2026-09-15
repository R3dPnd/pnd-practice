import importlib
import os
from collections import Counter

import pytest


def _load_impl():
    use_practice = os.environ.get("PRACTICE", "1") != "0"
    module_name = "practice_top_k_frequent_elements" if use_practice else "solution_top_k_frequent_elements"
    return importlib.import_module(module_name)


impl = _load_impl()


def test_classic_example():
    result = impl.top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert sorted(result) == [1, 2]


def test_single_element():
    assert impl.top_k_frequent([1], 1) == [1]


def test_returns_correct_count():
    result = impl.top_k_frequent([1, 1, 2, 2, 3, 3, 4], 3)
    assert len(result) == 3
    assert len(set(result)) == 3


def test_result_has_no_lower_frequency_than_excluded_elements():
    nums = [5, 5, 5, 5, 3, 3, 3, 2, 2, 1]
    counts = Counter(nums)
    k = 2
    result = impl.top_k_frequent(nums, k)

    result_freqs = sorted((counts[v] for v in result), reverse=True)
    excluded_freqs = sorted(
        (counts[v] for v in counts if v not in result), reverse=True
    )
    min_included = min(result_freqs)
    max_excluded = max(excluded_freqs) if excluded_freqs else 0
    assert min_included >= max_excluded


def test_all_elements_unique_frequency_one():
    result = impl.top_k_frequent([1, 2, 3, 4], 2)
    assert len(result) == 2
    assert set(result).issubset({1, 2, 3, 4})


def test_rejects_k_less_than_one():
    with pytest.raises(ValueError):
        impl.top_k_frequent([1, 2, 3], 0)


def test_rejects_k_larger_than_distinct_count():
    with pytest.raises(ValueError):
        impl.top_k_frequent([1, 1, 2], 5)
