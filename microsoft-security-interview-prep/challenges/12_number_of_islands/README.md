# 12 — Number of Islands

**Theme:** grid BFS/DFS — the canonical "graph implicit in a 2D grid" problem. Very
commonly asked; tests whether you can do connected-components traversal cleanly and
avoid infinite loops / revisits.

## Problem

```python
def num_islands(grid: List[List[str]]) -> int:
    """grid[r][c] is '1' (land) or '0' (water). An island is a maximal group of
    '1's connected 4-directionally (up/down/left/right — NOT diagonally).
    Return the number of islands."""
```

## Examples

```
grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"],
]
num_islands(grid) -> 3
```

## Constraints

- 4-directional adjacency only — two land cells touching only diagonally are **not**
  the same island.
- `grid` may be empty (`[]` or `[[]]`) — return `0`.
- **Do not mutate the caller's `grid`.** It's tempting to flood-fill by overwriting
  visited `'1'`s with `'0'` in place — that's a real technique, but it's also a
  side-effecting API a reviewer would flag; use a separate `visited` set instead.

## Talking points

- BFS with a queue vs. DFS with recursion here are both O(rows × cols) — either is
  fine; be ready to say why (each cell is visited/enqueued at most once).
- Recursive DFS risks a stack overflow on a very large grid (e.g. one giant island in
  a 1000×1000 grid) — an iterative BFS/DFS with an explicit stack/queue avoids that.
  Worth mentioning even if you implement the recursive version first.

## Run

```bash
pytest challenges/12_number_of_islands -v
```
