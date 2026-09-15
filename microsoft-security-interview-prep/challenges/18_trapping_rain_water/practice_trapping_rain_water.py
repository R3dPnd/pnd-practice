"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/18_trapping_rain_water -v` to check yourself, or
`PRACTICE=0 pytest challenges/18_trapping_rain_water -v` to see the reference
solution's tests pass instead.
"""
from typing import List


def trap(height: List[int]) -> int:

    count = 0
    
    n = len(height)
    max_l, max_r = [0]*n,[0]*n

    local_max = height[0]
    for hl in range(0,n-1):
        local_max = max(local_max, height[hl])
        max_l[hl] = local_max

    local_max = height[-1]
    for hr in range(len(height)-1, 1, -1):
        local_max = max(local_max, height[hr])
        max_r[hr] = local_max

    print(f"{max_l}:{max_r}:{height}")

    for h in range(1, n-1):
        curr = height[h]
        min_wall = min(max_l[h], max_r[h])
        if curr < min_wall:
            count += min_wall - curr
        print(curr)

    return curr
    
