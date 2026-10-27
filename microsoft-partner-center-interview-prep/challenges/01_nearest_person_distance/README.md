# 01 — Nearest Person Distance (Multi-Source BFS)

**Theme:** this is the "social distance" question from your Microsoft Security loop
(`../microsoft-security-interview-prep/interview/q1.py`). It comes first because it
already went wrong once in a real interview. Grid BFS is also one of the most reported
Microsoft coding topics. Same pattern as LeetCode 286 *Walls and Gates* and 542 *01 Matrix*.

## Problem

An office floor is a rectangular grid of single-character strings:

- `"P"`: an office with a person in it
- `"E"`: an empty, open office
- `"L"`: a locked office (impassable)

For every cell, return the number of steps to the **nearest** person, moving
up/down/left/right through non-locked cells.

```python
def nearest_person_distance(building: List[List[str]]) -> List[List[int]]:
    ...
```

## Output rules

- `"P"` cells → `0`
- `"E"` cells → shortest step count to any `"P"`, or `-1` if no person can reach it
- `"L"` cells → `-1`
- Return a **new** grid. Don't mutate `building`.

## Constraints

- The grid may be non-square (`rows != cols`). The tests check this.
- An empty grid (`[]`) returns `[]`.
- Ragged rows, or any character other than `P`/`E`/`L`, → `ValueError`.
- Up to ~250k cells. The intended solution is **O(rows × cols)**.

## Hints

- Don't BFS once per person. Seed **one** queue with **every** person at distance 0
  and run BFS once. Each wave of the BFS is one step further from the nearest person,
  so the first time you reach a cell is already its minimum distance.
- Edges are unweighted, so you don't need a heap or Dijkstra. Use a plain `deque` with
  `popleft()`, not `list.pop()`, which pops from the end and turns BFS into DFS.
- Mark a cell visited **when you enqueue it**, not when you dequeue it.

## What went wrong in q1.py (read after your own attempt)

<details>
<summary>Spoilers</summary>

Verified by running it. On its own 3×3 example it returns `[[1, 1, inf]] * 3`, and on a
2×3 grid it raises `IndexError`.

1. `[[INF] * len(building)] * len(building[0])`: the outer `*` copies **one row
   object** N times, so every row is the same list. The init loop's last row
   overwrites everything, and the person cells end up `INF`. The dimensions are also
   swapped (cols × rows), which is the `IndexError` on non-square grids. Use
   `[[x] * cols for _ in range(rows)]`.
2. Bug #1 hides a second bug. It pushes `(0, person)`, computes `new_d = 1`, and only
   expands if `dist[person] > 1`. With a correct init, `dist[person]` is `0`, so the
   search never leaves the start. The only reason it expanded at all was the aliasing
   bug resetting people to `INF`. That's also why people show up as `1`, not `0`.
3. Running a heap search per person is O(P · R · C · log) when one multi-source BFS
   is O(R · C). The "what if 100x bigger" follow-up would have exposed this.
4. Small things interviewers notice: typos in names (`person_distace`, `distace`),
   `queue.pop()` taking from the end of the list, and no handling for empty or ragged input.
   (Your version used `B` for empty. This one uses `E`.)

</details>

## Run

```bash
pytest challenges/01_nearest_person_distance -v
```
