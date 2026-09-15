"""Reference solution — see README.md for the problem statement.

WALKTHROUGH — how to arrive at this solution:
1. Reframe the problem: this is "count connected components" on an implicit graph,
   where every land cell (`'1'`) is a node and 4-directional adjacency defines the
   edges — recognizing that reframing is most of the battle.
2. Scan every cell in row-major order. Whenever an unvisited `'1'` is found, that's
   the discovery of a brand-new island — increment the island count, then flood-fill
   outward from it (BFS here) marking every reachable `'1'` as visited so none of
   them get counted again as a "new" island later in the scan.
3. BFS via an explicit queue (`deque`): pop a cell, check its four neighbors, enqueue
   any that are in-bounds, land, and not yet visited.
4. The outer double loop plus the inner BFS together still visit each cell a bounded
   number of times overall — not a quadratic blowup, because `visited` prevents
   re-processing.

COMMON INTERVIEWER FOLLOW-UPS:
- "BFS or DFS — does it matter here?" — no difference in correctness or asymptotic
  complexity for counting islands. BFS avoids Python's recursion depth limit on a
  very large/long island, which is the practical reason to prefer it over recursive
  DFS for this specific language.
- "What's the complexity?" — O(rows * cols) time and space — every cell is visited a
  constant number of times, and `visited` is sized to the grid.
- "How would you get this down to O(1) extra space?" — mutate the grid in place
  (flip visited `'1'`s to `'0'` or another sentinel) instead of maintaining a separate
  `visited` set — the tradeoff is that you can no longer treat the input as read-only.
- "How would this change for 8-directional adjacency (including diagonals)?" — add
  the four diagonal offsets to the neighbor-delta tuple; everything else is identical.
"""
from collections import deque
from typing import List, Set, Tuple


def num_islands(grid: List[List[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited: Set[Tuple[int, int]] = set()
    islands = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1" or (r, c) in visited:
                continue

            islands += 1
            queue = deque([(r, c)])
            visited.add((r, c))

            while queue:
                cr, cc = queue.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = cr + dr, cc + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] == "1"
                        and (nr, nc) not in visited
                    ):
                        visited.add((nr, nc))
                        queue.append((nr, nc))

    return islands
