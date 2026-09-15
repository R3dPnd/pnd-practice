"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/15_top_k_frequent_elements -v` to check yourself, or
`PRACTICE=0 pytest challenges/15_top_k_frequent_elements -v` to see the
reference solution's tests pass instead.
"""
from typing import Counter, List


def top_k_frequent(nums: List[int], k: int) -> List[int]:
    if k<1:
        return []

    counts = Counter(nums)

    if len(counts) < k:
        return []
    resp = []

