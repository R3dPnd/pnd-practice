# 07 — Grid Flood Fill

**Theme:** grid BFS/DFS. Matches Disney's LeetCode-tagged **"Flood Fill"** directly, and
the same multi-source grid-BFS pattern as their tagged **"Walls and Gates."**

## Problem

```js
export function floodFill(image, sr, sc, color) {
  /* image is a 2D array of ints. Starting at (sr, sc), replace the connected
     region of cells with the SAME color as the starting cell (4-directionally
     connected: up/down/left/right, not diagonal) with `color`. Returns the
     mutated image. */
}
```

## Constraints / edge cases to think about

- If the starting cell already has `color`, return immediately — flooding it "again"
  with an iterative/recursive approach that doesn't check this first will infinite-loop.
- Stay within grid bounds; don't wrap around edges.
- Only connected cells matching the *original* start color get repainted — a
  same-colored region that isn't reachable from `(sr, sc)` must stay untouched.

## Extension (not covered by the tests here, but worth talking through out loud)

**"Walls and Gates"** is the same core pattern one level up: instead of a single BFS
from one start cell, you run a **multi-source BFS** starting from *every* gate cell at
once, filling each empty room with its distance to the nearest gate. If asked, describe
it as: push all gates onto the queue first (distance 0), then BFS outward exactly like
`floodFill`, except you're writing distances instead of a color, and cells marked as
walls block traversal instead of needing to match a color.

## Why this matters for FE

Grid BFS is a stand-in for graph problems generally, and shows up in real FE-adjacent
work more than you'd expect: computing which cells to highlight in a spreadsheet-like
grid, contiguous-selection logic (click-drag select in a calendar/seating chart), or a
minimap/pathfinding feature. It's also just a fast, unambiguous way for an interviewer
to check traversal correctness and boundary-condition discipline.

## Run

```bash
node --test challenges/07_grid_flood_fill -v
```
