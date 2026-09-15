"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/09_two_sum -v` to check yourself, or
`PRACTICE=0 pytest challenges/09_two_sum -v` to see the reference
solution's tests pass instead.
"""
from typing import List


def two_sum(nums: List[int], target: int) -> List[int]:
    seen_values = {}
    for i,v in enumerate(nums):
        rem = target - v
        if rem in seen_values:
            return [seen_values[rem], i]
        seen_values[v] = i
    raise ValueError("no two numbers sum to target")
