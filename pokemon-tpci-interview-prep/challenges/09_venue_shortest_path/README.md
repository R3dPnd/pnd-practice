# 09 — Shortest path across the venue floor

**Pattern:** grid BFS · **Classic** (Shortest Path in Binary Matrix / maze)

A Worlds venue floor map is a grid: `.` open, `#` blocked (stage, barriers), `S` start,
`E` exit. Movement is 4-directional.

## Task
`ShortestPath(grid []string) int` — fewest steps from `S` to `E`, or `-1` if unreachable
(or if `S`/`E` is missing).

## Follow-ups to be ready for
- Return the actual path (store parent pointers).
- Count islands of open floor (connected components — same BFS/DFS).
- Weighted cells (crowded areas cost more) → Dijkstra with `container/heap`.
