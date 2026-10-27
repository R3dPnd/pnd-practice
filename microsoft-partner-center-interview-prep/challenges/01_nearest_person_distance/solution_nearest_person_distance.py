"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Brute force: for every empty cell, BFS outward until you hit a person, which is
   O((R*C)^2). The flipped version, one BFS *from* each person, is O(P*R*C) and still
   too slow when the floor is mostly people. State the brute force out loud, then improve it.
2. Key insight: you want each cell's distance to the *nearest* source, and the edges
   are unweighted. Put every source in the queue at distance 0 and run a single BFS.
   BFS reaches cells in order of distance, so the first time it reaches a cell is
   already the minimum. You never need to overwrite a distance.
3. Use `-1` as both "not visited yet" and "unreachable". After BFS, any `E` still at
   -1 was never reached. `L` cells are never enqueued, so they stay -1.

COMMON INTERVIEWER FOLLOW-UPS:
- "Complexity?" — O(R*C) time: each cell is enqueued at most once and checks 4
  neighbors. O(R*C) space for the output and the queue.
- "Why not Dijkstra / a heap?" — all edges weigh 1, so BFS order already is distance
  order and a heap only adds a log factor. If locked doors had a weighted unlock cost,
  you'd switch to Dijkstra (or 0-1 BFS if costs are only 0/1).
- "Return the *nearest person's id* instead of the distance?" — carry the source id
  through the queue: `(r, c, source_id)`. Same complexity.
- "Grid too big for memory?" — process in row bands and exchange boundary distances
  between bands. Mostly a talking point, not something to code here.
- "Diagonal moves?" — add the 4 diagonal deltas. With 8 directions this is still BFS
  (Chebyshev distance).
"""
from collections import deque
from typing import Deque, List, Tuple

_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))
_VALID = {"P", "E", "L"}


def nearest_person_distance(building: List[List[str]]) -> List[List[int]]:
    if not building:
        return []
    rows, cols = len(building), len(building[0])

    dist = [[-1] * cols for _ in range(rows)]
    queue: Deque[Tuple[int, int]] = deque()

    for r, row in enumerate(building):
        if len(row) != cols:
            raise ValueError(f"row {r} has length {len(row)}, expected {cols}")
        for c, cell in enumerate(row):
            if cell not in _VALID:
                raise ValueError(f"invalid cell {cell!r} at ({r}, {c})")
            if cell == "P":
                dist[r][c] = 0
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in _DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < rows
                and 0 <= nc < cols
                and building[nr][nc] == "E"
                and dist[nr][nc] == -1
            ):
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
