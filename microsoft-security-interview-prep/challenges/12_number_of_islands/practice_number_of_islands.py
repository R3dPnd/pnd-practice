"""Fill this in. See README.md for the problem statement.

Run `pytest challenges/12_number_of_islands -v` to check yourself, or
`PRACTICE=0 pytest challenges/12_number_of_islands -v` to see the reference
solution's tests pass instead.
"""
from typing import List


def num_islands(grid: List[List[str]]) -> int:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if not grid or not grid[0]:
        return 0
    count = 0
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def dfs(x, y):
        visited.add((x,y))
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and (new_x,new_y) not in visited and grid[new_x][new_y] == "1":
                dfs(new_x, new_y)

    for x in range(rows):
        for y in range(cols):
            if (x,y) in visited:
                continue
            elif grid[x][y] == "1":
                dfs(x, y)
                count += 1
    return count
