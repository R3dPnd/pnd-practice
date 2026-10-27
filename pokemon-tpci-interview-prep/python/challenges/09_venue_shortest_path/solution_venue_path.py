"""Shortest path across the venue floor — reference solution (BFS).

Why BFS? Every step costs the same (1). Breadth-first search explores cells in rings:
first everything 1 step away, then everything 2 steps away, and so on. So the FIRST time
BFS reaches the exit, it got there by a shortest path. (DFS gives no such guarantee.)

Time O(rows * cols): each cell is enqueued at most once. Space is the same.
"""
from collections import deque


def shortest_path(grid: list[str]) -> int:
    # ---- Find S and E ----
    start = end = None
    for r, row in enumerate(grid):          # enumerate gives (index, value) pairs
        for c, ch in enumerate(row):        # strings are iterable character by character
            if ch == "S":
                start = (r, c)
            elif ch == "E":
                end = (r, c)
    if start is None or end is None:
        return -1

    # `dist` does double duty:
    #   1. the distance from S to each discovered cell
    #   2. the "visited" set (if a cell is in dist, we've already queued it)
    dist = {start: 0}

    # deque gives O(1) popleft. list.pop(0) would be O(n) — a classic BFS performance bug.
    queue = deque([start])

    while queue:
        # FIFO: take the OLDEST queued cell. This is what makes it breadth-first.
        r, c = queue.popleft()

        # Reached the exit → its distance is the shortest one (see the docstring).
        if (r, c) == end:
            return dist[(r, c)]

        # Try the 4 neighbors: down, up, right, left.
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < len(grid)            # row is inside the grid
                and 0 <= nc < len(grid[nr])    # column is inside that row
                and grid[nr][nc] != "#"        # not a wall
                and (nr, nc) not in dist       # not already discovered
            ):
                # Mark it discovered WHEN WE ENQUEUE it, not when we dequeue it.
                # Otherwise the same cell can be queued many times from different neighbors.
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))

    # The queue ran dry without reaching E → it's walled off.
    return -1
