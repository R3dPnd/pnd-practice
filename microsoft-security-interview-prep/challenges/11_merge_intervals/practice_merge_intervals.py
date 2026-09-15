"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/11_merge_intervals -v` to check yourself, or
`PRACTICE=0 pytest challenges/11_merge_intervals -v` to see the reference
solution's tests pass instead.
"""
from typing import List


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    if not intervals:
        return []
    sorted_interval = sorted(intervals,key=lambda x: x[0])
    merged = [list(sorted_interval[0])]
    for curr in sorted_interval[1:]:
        # If the current interval overlaps with the previous one, merge them
        prev = merged[-1]
        if curr[0] <= prev[1]:
            prev[1] = max(prev[1], curr[1])
        else:
            merged.append(list(curr))
        
    return merged